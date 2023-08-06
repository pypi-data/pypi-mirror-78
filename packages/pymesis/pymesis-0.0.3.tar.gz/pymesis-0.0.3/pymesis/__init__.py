"""
Memoization for Python, with optional TTL (measured in time or function call count) for the cached results.
"""


__author__ = 'Daniel Hjertholm'
__version__ = '0.0.3'


from .pymesis import memoize, TTLUnit


__all__ = (memoize, TTLUnit)
