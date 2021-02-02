def my_map(func, iterator):
    return (func(i) for i in iterator)


def func(i):
    return int(i)


lst = '123456789'.split()
print(list(my_map(func, lst)))


from functools import wraps
from time import perf_counter
import logging
logging.basicConfig(level=logging.DEBUG, 
                    filename='test.log', 
                    datefmt='%Y-%m-%d %H:%M:%S', 
                    format='[%(asctime)s]-%(levelname)s-%(message)s')


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = perf_counter()
        r = func(*args, **kwargs)
        t1 = perf_counter()
        logging.info(f'time_elapsed: {t1 - t0}')
        return r
    return wrapper


@timer
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)


print(fib(5))