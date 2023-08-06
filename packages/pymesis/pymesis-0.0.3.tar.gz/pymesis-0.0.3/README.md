# pymesis
Memoization decorator for Python, with optional TTL (measured in time or function calls) for the cached results.

## Installation

Using pipenv (recommended):

```shell
pipenv install pymesis
```

Using pip:

```shell
pip install pymesis
```


## Usage

Basic usage:

```python
from pymesis import memoize
from time import time, sleep

@memoize
def slowFunction(*args, **kwargs):
    sleep(1)
    return 'Completed'

start = time()
print(slowFunction('some', 'data')
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # First call is slow

start = time()
print(slowFunction('some', 'data')
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # Second call is fast, as data is cached

start = time()
print(slowFunction('some', 'new', 'data')
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # This call is slow, as attributes have changed
```

With TTL:

```python
from pymesis import memoize, TTLUnit
from time import time, sleep

@memoize(ttl=1, ttl_unit=TTLUnit.CALL_COUNT) # Only return cached result once, then go back to calling flowFunction
def slowFunction(*args, **kwargs):
    sleep(1)
    return 'Completed'

start = time()
print(slowFunction('some', 'data')
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # First call is slow

start = time()
print(slowFunction('some', 'data')
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # Second call is fast

start = time()
print(slowFunction('some', 'data')
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # Third call is slow, as cache has expired (TTL=1).
```

Note that functions are assumed to be unchanged as long as the name is unchanged. Redefined function (with decorator applied again) will return cached result of similar call to the original function.

The decorator works with methods as well as functions. Note that the same method on two different instances of the same class are considered different methods, therefore a call to the second will not give the cached result from the first. 

<!--
TODO:

How it works

Build status
-->
