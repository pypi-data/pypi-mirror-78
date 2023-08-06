#!/usr/bin/env python3

from logging import getLogger
from socket import (
    AF_INET,
    IPPROTO_TCP,
    SO_KEEPALIVE,
    SOCK_STREAM,
    SOL_SOCKET,
    TCP_KEEPCNT,
    TCP_KEEPIDLE,
    TCP_KEEPINTVL,
    SHUT_RDWR,
    getaddrinfo,
    socket,
)
from threading import Timer
from time import sleep
from signal import signal, SIGTERM

from .resource_balancer import ResourceBalancer

from ph_wsgiref.simple_server import WSGIRequestHandler

LOGGER = getLogger('pothead.worker')


class Handler(WSGIRequestHandler):
    protocol_version = "HTTP/1.1"

    def handle_one_request(self):
        try:
            super().handle_one_request()
        finally:
            self.close_connection = True

    def parse_request(self):
        res = super().parse_request()

        # This socket shall no longer be fast-closed on SIGTERM
        socket = self.request
        self.server.sockets_waiting_for_request.remove(socket)

        return res

class Server:
    ssl_context = None
    multithread = False
    multiprocess = False
    server_address = "localhost"
    passthrough_errors = False
    shutdown_signal = False
    running = True

    def __init__(self, addr, app):
        (host, port) = addr
        # Set up base environment
        env = self.base_environ = {}
        env["SERVER_NAME"] = host
        env["GATEWAY_INTERFACE"] = "HTTP/1.1"
        env["SERVER_PORT"] = port
        env["REMOTE_HOST"] = ""
        env["CONTENT_LENGTH"] = ""
        env["SCRIPT_NAME"] = ""

        self.balancer = LoadBalancer(host, port)
        self.app = app
        self.sockets_waiting_for_request = set()

    def run(self):
        while self.running:
            with socket(
                AF_INET, SOCK_STREAM
            ) as s, self.balancer.acquire_addr() as addr:
                self.sockets_waiting_for_request.add(s)
                try:
                    s.connect(addr)

                    s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
                    s.setsockopt(IPPROTO_TCP, TCP_KEEPIDLE, 1)
                    s.setsockopt(IPPROTO_TCP, TCP_KEEPINTVL, 2)
                    s.setsockopt(IPPROTO_TCP, TCP_KEEPCNT, 3)
                except Exception as e:
                    LOGGER.error("Connect To Broker: %s", e)
                    sleep(2)
                    continue

                try:
                    Handler(s, addr, self)
                except:
                    LOGGER.exception("In WSGI request handling")
                    sleep(1)
                    continue

    def get_app(self):
        return self.app

    def shutdown(self):
        LOGGER.info("shutting down workers...")
        self.running = False
        for s in list(self.sockets_waiting_for_request):
            s.shutdown(SHUT_RDWR)
            s.close()


def install_term_handler(f):
    previous = []
    def on_term(_signal, _stack):
        f()
        for p in previous:
            p()
    p = signal(SIGTERM, on_term)
    if p:
        previous.append(p)


class LoadBalancer:
    REFRESH_INTERVAL = 5

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._balancer = ResourceBalancer()
        self.refresh()

    def acquire_addr(self):
        return self._balancer.acquire()

    def refresh(self):
        try:
            results = getaddrinfo(self.host, self.port, type=SOCK_STREAM)
            hosts = (sockaddr for _f, _t, _p, _c, sockaddr in results)
            self._balancer.provision(hosts)
        except:
            LOGGER.exception("Failed to refresh endpoints for %s:%d", self.host, self.port)
        t = Timer(self.REFRESH_INTERVAL, self.refresh)
        t.setDaemon(True)
        t.start()


if __name__ == "__main__":
    from argparse import ArgumentParser
    from importlib import import_module
    from threading import Thread
    from sys import path
    from logging import basicConfig, INFO

    path.insert(0, ".")

    def address(str):
        (host, port) = str.rsplit(":", 1)
        return (host, int(port))

    def func(str):
        (module, symbol) = str.rsplit(":", 1)
        module = import_module(module)
        return getattr(module, symbol)

    parser = ArgumentParser(description="Run WSGI app in sequential `worker` mode")
    parser.add_argument(
        "--connect",
        default="localhost:4040",
        type=address,
        help="Load Balancer Hub to connect to [host:port]",
    )
    parser.add_argument(
        "--workers", default=1, type=int, help="Number of worker Processes"
    )
    parser.add_argument(
        "app",
        nargs="?",
        default="wsgiref.simple_server:demo_app",
        type=func,
        help="The WSGI request handler to handle requests",
    )
    args = parser.parse_args()
    basicConfig(level=INFO)

    LOGGER.info("Initializing server for app %s", args.app)

    server = Server(args.connect, args.app)

    install_term_handler(server.shutdown)

    LOGGER.info("Starting up %d workers connecting to %s", args.workers, args.connect)

    workers = [Thread(target=server.run) for _ in range(args.workers)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()

    LOGGER.info("shut down")
