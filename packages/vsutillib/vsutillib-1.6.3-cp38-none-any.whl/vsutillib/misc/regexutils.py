"""
Regular Expresions utils
"""

import re


def multipleReplace(aDict, text):
    # Create a regular expression from all of the dictionary keys
    regex = re.compile("|".join(map(re.escape, aDict.keys())))

    # For each match, look up the corresponding value in the dictionary
    return regex.sub(lambda match: aDict[match.group(0)], text)
