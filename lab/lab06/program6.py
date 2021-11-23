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
            t = (end-start)/n
            
            console.print(f'Average execution time of {func.__name__} after {n} iterations: {t*1000} ms')
            
            return result
        
        return wrapper
    
    if _func is not None:
        return decorator(_func)
    
    return decorator

@timeit(n = 2)
def f1(x):
    time.sleep(1)
    return (x**2 - x*(x + 5) + np.cos(x))

console = Console()
console.clear()
rich.traceback.install()

a = f1(8)

