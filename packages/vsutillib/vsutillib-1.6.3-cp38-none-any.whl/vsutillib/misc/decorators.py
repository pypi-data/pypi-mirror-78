"""
Decorators found on internet
"""


import functools


def callCounter(func):
    """function call counter"""

    @functools.wraps(func)
    def helper(*args, **kwargs):
        helper.calls += 1
        return func(*args, **kwargs)
    helper.calls = 0

    return helper

def staticVars(**kwargs):
    """Add static variables to function"""

    def decorate(func):
        """Add attributes to func"""
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate
