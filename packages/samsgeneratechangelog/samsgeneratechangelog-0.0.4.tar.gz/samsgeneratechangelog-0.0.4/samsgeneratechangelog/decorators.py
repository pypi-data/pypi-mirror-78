from functools import update_wrapper
import logging


class DebugOutput:

    def __init__(self, func, type_=None):
        self.func = func
        self.type = type_
        update_wrapper(self, func)

    def __get__(self, obj, type_=None):
        return self.__class__(self.func.__get__(obj, type_), type_)

    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        logging.debug(f"Returned {len(result)} values from {self.func.__name__}")
        return result
