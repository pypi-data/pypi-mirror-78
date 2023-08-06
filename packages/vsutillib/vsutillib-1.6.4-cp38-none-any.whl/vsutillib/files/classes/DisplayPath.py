"""
pretty print tree
"""

from pathlib import Path

from natsort import natsorted, ns


class Prefix:

    filenameMiddle = "├──"
    filenameLast = "└──"
    parentMiddle = "    "
    parentLast = "│   "

    # filenameMiddle = "├─"
    # filenameLast = "└─"
    # parentMiddle = "  "
    # parentLast = "│ "


class DisplayPath:
    """DisplayPath"""

    def __init__(self, path, parentPath, isLast):
        self.path = Path(str(path))
        self.parentPath = parentPath
        self.isLast = isLast
        if self.parentPath:
            self.depth = self.parentPath.depth + 1
        else:
            self.depth = 0

    @classmethod
    def makeTree(cls, root, parent=None, isLast=False, criteria=None, fileList=None):
        """makeTree"""

        root = Path(str(root))
        criteria = criteria or cls._defaultCriteria

        displayableRoot = cls(root, parent, isLast)
        yield displayableRoot

        childNames = []
        if fileList is not None:
            for oFile in fileList:
                childNames.append(oFile.name)
            children = natsorted(fileList, alg=ns.PATH)
        else:
            children = natsorted(
                list(path for path in root.iterdir() if criteria(path)), alg=ns.PATH,
            )
        count = 1
        for path in children:
            isLast = count == len(children)
            if path.is_dir():
                yield from cls.makeTree(
                    path, parent=displayableRoot, isLast=isLast, criteria=criteria
                )
            else:
                yield cls(path, displayableRoot, isLast)
            count += 1

    @classmethod
    def _defaultCriteria(cls, path):  # pylint: disable=unused-argument
        return True

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + "/"
        return self.path.name

    def displayable(self):
        """displayable"""

        if self.parentPath is None:
            return self.displayname

        _filename_prefix = Prefix.filenameLast if self.isLast else Prefix.filenameMiddle

        parts = ["{!s} {!s}".format(_filename_prefix, self.displayname)]

        parent = self.parentPath
        while parent and parent.parentPath is not None:
            parts.append(Prefix.parentMiddle if parent.isLast else Prefix.parentLast)
            parent = parent.parentPath

        return "".join(reversed(parts))
