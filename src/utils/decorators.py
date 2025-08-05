from typing import Any, Callable


def static_vars(**kwargs: Any) -> Callable:
    def decorate(func: Callable) -> Callable:
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate
