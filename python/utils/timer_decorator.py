import time
from functools import wraps


def timer_decorator(args1):
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            initial = time.time()
            result = function(*args, **kwargs)
            ends = time.time()
            print(f"{args1}:" + str(ends - initial))
            return result

        return wrapper

    return inner_function
