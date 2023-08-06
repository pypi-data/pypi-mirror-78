import warnings
from functools import wraps

class Uninstalled:
    def __init__ (self, name, *args, **kargs):
        self.name = name

    def __call__ (self, *args, **kargs):
        raise ImportError ('cannot import {}, install first'.format (self.name))

def deprecated (msg = ""):
    def decorator (f):
        @wraps(f)
        def wrapper (*args, **kwargs):
            nonlocal msg

            warnings.simplefilter ('default')
            warnings.warn (
               "{} will be deprecated{}".format (f.__name__, msg and (", " + msg) or ""),
                DeprecationWarning
            )
            return f (*args, **kwargs)
        return wrapper

    if isinstance (msg, str):
        return decorator
    f, msg = msg, ''
    return decorator (f)

def override (f):
    @wraps (f)
    def wrapper (*args, **karg):
        return f (*args, **karg)
    return wrapper
