"""All decorators used by the module."""
from functools import update_wrapper
import logging


class DebugOutput:
    """Decorate a method to provide debug output about what is returned from a method."""

    def __init__(self, func, type_=None):
        """Initialises DebugOutput."""
        self.func = func
        self.type = type_
        update_wrapper(self, func)

    def __get__(self, obj, type_=None):
        """Return a bound version of the method that we're decorating."""
        return self.__class__(self.func.__get__(obj, type_), type_)

    def __call__(self, *args, **kwargs):
        """Execute the decorated method and log the number of results."""
        result = self.func(*args, **kwargs)
        logging.debug(f"Returned {len(result)} values from {self.func.__name__}")
        return result
