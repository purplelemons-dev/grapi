from typing import Iterator, Callable


__all__ = ["Headers"]


def format_name(name: str) -> str:
    return name.replace("_", "-").lower()


class Headers:

    def __init__(self, **kwargs: dict[str, str]):
        self.headers: dict[str, str] = {}

        for name, value in kwargs.items():
            self.headers[format_name(name)] = value

    def __str__(self) -> str:
        return "\r\n".join(f"{name}: {value}" for name, value in self.headers.items())

    def __getitem__(self, key: str) -> str:
        return self.headers[format_name(key)]

    def __setitem__(self, key: str, value: str) -> None:
        self.headers[format_name(key)] = value

    def __delitem__(self, key: str) -> None:
        del self.headers[format_name(key)]

    def __iter__(self) -> Iterator[str]:
        return iter(self.headers)
