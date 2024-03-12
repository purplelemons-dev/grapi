import socketserver
import socket
from typing import Callable
from .reqres import Request, Response

SERVER_CHUNK_SIZE = 4 * 1024


class Handler(socketserver.BaseRequestHandler):
    request: socket.socket
    routes: dict

    def handle(self):
        self.data = self.request.recv(SERVER_CHUNK_SIZE).strip()
        self.method, self.path, *_ = self.data.decode().split("\r\n")[0].split(" ")
        self.headers = self.data.decode().split("\r\n")[1:]
        self._request = Request(self.method, self.path, self.headers)
        self._response = Response(self.request)
        self.route_request()

    def route_request(self):
        try:
            response_function: Callable[[Request, Response], Response] = self.routes[self.method][
                self.path
            ]
            self.response = response_function(self._request, self._response)
        except KeyError:
            self.response.status_code = 404
            self.response.body = "Not Found"
        self.request.sendall(self.response.encode())


class Server(socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(self, host: str = "localhost", port: int = 8080) -> None:
        self.handler = Handler
        self.handler.routes = {
            "GET": {},
            "POST": {},
            "PUT": {},
            "PATCH": {},
            "DELETE": {},
            "HEAD": {},
        }
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
