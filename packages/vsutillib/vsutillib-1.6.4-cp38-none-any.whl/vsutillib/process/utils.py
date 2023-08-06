"""
Convenience functions
"""

import threading


def isThreadRunning(threadName):
    """
    isThreadRunning check for named thread running

    Args:
        threadName (str): name of thread to look for

    Returns:
        bool: True if name found, False otherwise.
    """

    if threadName in [x.name for x in threading.enumerate()]:
        return True

    return False
