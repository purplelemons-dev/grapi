import jinja2
from .headers import Headers
from .__version__ import __version__


class Request:
    def __init__(self, path: str, headers: Headers, body: str) -> None:
        self.path = path
        self.headers = headers
        self.body = body


class Response:
    def __init__(self, views_dir="./views", http_protocol_version="HTTP/1.1") -> None:
        self.views_dir = views_dir
        self.http_protocol_version = http_protocol_version
        self.headers: Headers = Headers(
            server=f"GrAPI/{__version__}", content_type="text/plain", content_length="0"
        )
        self.status_code = 200
        self.status_message = "OK"
        self.body = ""

    def __call__(self) -> str:
        self.headers["content-length"] = str(len(self.body))
        out = (
            f"{self.http_protocol_version} {self.status_code} {self.status_message}\r\n"
        )
        out += str(self.headers)
        out += f"\r\n\r\n{self.body}"
        return out

    def status(self, code: int):
        self.status_code = code
        return self

    def text(self, text: str):
        self.body = text
        return self

    def file(self, file: str):
        with open(file, "r") as f:
            self.body = f.read()
        return self

    def render(self, **kwargs):
        self.body = jinja2.Template(self.body).render(**kwargs)
        return self

    def _view(self, path: str, **kwargs):
        if path.startswith("/"):
            path = path[1:]

        if "." not in path.split("/")[-1]:
            self.file(f"{self.views_dir}/{path}.html")
            self.headers["content-type"] = "text/html"
            self.body.replace(
                "</head>", f"<link rel='stylesheet' href='{path}.css'></head>"
            )
            self.body += f"<script src='{path}.js'></script>"
            self.render(**kwargs)
        elif path.endswith(".css"):
            self.headers["content-type"] = "text/css"
            self.file(f"{self.views_dir}/{path}/.css")
        elif path.endswith(".js"):
            self.headers["content-type"] = "text/javascript"
            self.file(f"{self.views_dir}/{path}/.js")
        return self
