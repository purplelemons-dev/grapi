from typing import Iterator, Callable


__all__ = ["Headers"]


def ensure_format_name(func: Callable) -> Callable:
    def wrapper(self: Headers, name: str, *args, **kwargs):
        return func(self, format_name(name), *args, **kwargs)

    return wrapper


def format_name(name: str) -> str:
    return name.replace("_", "-").lower()


class Headers:

    @staticmethod
    def __init__(self, **kwargs: dict[str,str]):
        self._headers = {}

        for name, value in kwargs.items():
            self._headers[format_name(name)] = value

    def __getitem__(self, key: str) -> str:
        return self._headers[key]

    def __setitem__(self, key: str, value: str) -> None:
        self._headers[key] = value

    def __delitem__(self, key: str) -> None:
        del self._headers[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._headers)

    @ensure_format_name
    def __getattr__(self, name: str) -> str:
        return self._headers[name]

    @ensure_format_name
    def __setattr__(self, name: str, value: str) -> None:
        self._headers[name] = value

    @ensure_format_name
    def __delattr__(self, name: str) -> None:
        del self._headers[name]
