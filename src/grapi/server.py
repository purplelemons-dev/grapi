import socketserver
import socket
from typing import Callable
from .reqres import Request, Response
from .headers import Headers

SERVER_CHUNK_SIZE = 4 * 1024


class Handler(socketserver.BaseRequestHandler):
    request: socket.socket
    routes: dict
    views_dir: str
    protocol_version: str

    def handle(self):
        self.data = self.request.recv(SERVER_CHUNK_SIZE).strip().decode()
        self.method, self.path, *_ = self.data.split("\r\n")[0].split(" ")
        self.body = "\r\n\r\n".join(self.data.split("\r\n\r\n")[1:])
        # hot garbage dont look plz
        self.headers = {
            header: ":".join(value)
            for header, *value in [
                split.replace(": ", ":", 1).split(":")
                for split in self.data.split("\r\n")[1:]
            ]
        }
        self._request = Request(self.path, Headers(**self.headers), self.body)
        self._response = Response(self.views_dir, self.protocol_version)
        self.route_request()

    def route_request(self):
        try:
            response_function: Callable[[Request, Response], Response] = self.routes[
                self.method
            ][self.path]
            response = response_function(self._request, self._response)
            self.request.sendall(response().encode())
        except KeyError:
            self.request.sendall(self._response._view(path=self.path)().encode())


class Server(socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        http_version: str = "HTTP/1.1",
        views_dir: str = "./views",
    ) -> None:
        self.handler = Handler
        self.handler.routes = {
            "GET": {},
            "POST": {},
            "PUT": {},
            "PATCH": {},
            "DELETE": {},
            "HEAD": {},
        }
        self.handler.views_dir = views_dir
        self.handler.protocol_version = http_version
        super().__init__((host, port), self.handler)

    def __call__(self, path: str):
        def decorator(func: Callable[[Request, Response], Response]) -> Callable:
            self.handler.routes[func.__name__][path] = func

        return decorator

    def run(self):
        addr, port = self.server_address
        print(f"Server running on httP://{addr}:{port}")
        self.serve_forever()


if __name__ == "__main__":
    server = Server()
    server.run()
