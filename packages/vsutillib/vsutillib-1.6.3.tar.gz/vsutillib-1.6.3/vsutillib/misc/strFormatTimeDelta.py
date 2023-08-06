"""
format timedelta object
"""

from string import Formatter


def strFormatTimeDelta(tDelta, fmt=None):
    """
    strFormatTimeDelta format time delta string. If fmt is None a format of
    'N days N hours N minutes N seconds' will be used starting with the first
    non zero N found in the calculations.


    Args:
        tDelta (timedelta): timedelta object to format
        fmt (str, optional): string formatter. Defaults to None.

    Returns:
        str: formatted timedelta string
    """

    strFormatter = Formatter()
    args = {}
    divisor = {'W': 604800, 'D': 86400, 'H': 3600, 'M': 60, 'S': 1}
    labels = {'W': "weeks", 'D': "days", 'H': "hours", 'M': "minutes", 'S': "seconds"}

    remainder = int(tDelta.total_seconds())

    if fmt is not None:
        keywords = list(map(lambda x: x[1], list(strFormatter.parse(fmt))))
        for key in divisor:
            if key in keywords and key in divisor.keys():
                args[key], remainder = divmod(remainder, divisor[key])
    else:
        firstFound = False
        strTmp = ""
        for key in divisor:
            quotient, remainder = divmod(remainder, divisor[key])
            if firstFound:
                strTmp += " " + str(quotient) + " " + labels[key]
            elif quotient > 0:
                strTmp += str(quotient) + " " + labels[key]
                firstFound = True

    if fmt is None:
        return strTmp

    return strFormatter.format(fmt, **args)
