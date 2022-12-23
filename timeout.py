import errno
import os
import threading
import functools

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout():
            raise TimeoutError(error_message)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timer = threading.Timer(seconds, _handle_timeout)
            timer.start()
            try:
                result = func(*args, **kwargs)
            finally:
                timer.cancel()
            return result

        return wrapper

    return decorator
