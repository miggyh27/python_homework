# Task 1

import functools
import logging

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.propagate = False
if not logger.handlers:
    _handler = logging.FileHandler("./decorator.log", "a", encoding="utf-8")
    logger.addHandler(_handler)


def logger_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        pos = list(args) if args else "none"
        kw = dict(kwargs) if kwargs else "none"
        logger.log(logging.INFO, f"function: {func.__name__}")
        logger.log(logging.INFO, f"positional parameters: {pos}")
        logger.log(logging.INFO, f"keyword parameters: {kw}")
        logger.log(logging.INFO, f"return: {result}")
        return result

    return wrapper


@logger_decorator
def hello() -> None:
    print("Hello, World!")


@logger_decorator
def collect_positional(*args) -> bool:
    return True


@logger_decorator
def keyword_only(**kwargs):
    return logger_decorator


if __name__ == "__main__":
    hello()
    collect_positional(1, 2, "three")
    keyword_only(a=1, b="two")
