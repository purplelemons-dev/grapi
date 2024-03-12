import jinja2
from .headers import Headers
from .__version__ import __version__

class Request:
    def __init__(self) -> None:
        pass


class Response:
    def __init__(self, views_dir="./views", http_protocol_version="HTTP/1.1") -> None:
        self.views_dir = views_dir
        self.http_protocol_version = http_protocol_version
        self.headers: Headers = Headers(
            server=f"GrAPI/{__version__}",
            content_type="text/plain",
            content_length="0",
        )
    
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

    def _view(self, path:str, **kwargs):
        if path.startswith("/"):
            path = path[1:]
        
        if "." not in path.split("/")[-1]:
            self.file(f"{self.views_dir}/{path}.html")
            self.body.replace("</head>", f"<link rel='stylesheet' href='{path}.css'></head>")
            self.body += f"<script src='{path}.js'></script>"
            self.render(**kwargs)
        elif any(path.endswith(ext) for ext in [".css", ".js"]):
            self.file(f"{self.views_dir}/{path}".replace(".css", "/.css").replace(".js", "/.js"))
        return self


    def _encode(self):
