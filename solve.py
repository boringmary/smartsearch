import time
from functools import wraps


def decorator_capture(capture):
    def wrapper(func):
        def inner(boo, bar=None, **baz):
            arguments = {}
            arguments.update(baz, boo=boo, bar=bar)
            capture.append(arguments)
            print arguments

            return func(boo, bar, **baz)
        return inner
    return wrapper


def decorator_time(func):
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        return result, end-start
    return inner


def decorator_mimic(func):
    @wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner



def decorator_inc(func_or_inc=None):
    if hasattr(func_or_inc, '__call__'):
        def inner():
            return func_or_inc() + 1
        return inner
    else:
        def wrapper(func):
            def inner():
                return func() + func_or_inc
            return inner
        return wrapper
