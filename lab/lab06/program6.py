# poetry run python .\program6.py

from rich.console import Console
import rich.traceback
import functools
import numpy as np
import time

def timeit(_func = None, n = 10):
    
    def decorator(func):
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            
            start = time.time()
            
            for i in range(n):
                result = func(*args, **kwargs)

            end = time.time()
            t = (end-start)/n*1000
            
            console.print(f'Average execution time of {func.__name__} after {n} iterations: ' + "{:.3f}".format(t) + ' ms')
            
            return result
        
        return wrapper
    
    if _func is not None:
        return decorator(_func)
    
    return decorator

@timeit(n = 7)
def f1():
    time.sleep(0.5)


console = Console()
console.clear()
rich.traceback.install()

a = f1()

