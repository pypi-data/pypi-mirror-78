"""
 Parse the attachments from mkvmerge command line
 and gather all that is needed to add attachments

 Global:
  Apply the same attachments to all files.  If the application does
  not find enough directories in the parent directory of the supplied
  one or there are more than one directory for the attachments in
  the command line.

 Per File:
  If the application finds the same number of directories as
  the number of input files in the root of the supplied it will
  assumed is directory for each file.  The directories can be empty
  meaning corresponding file has no attachments.
"""

import re
import shlex

from pathlib import Path

from ..mkvutils import unQuote


class MKVAttachment:  # pylint: disable=too-few-public-methods
    """
    Class to save attachment information

    """

    def __init__(self, attachment, span=None, matchString=None):

        self.name = None
        self.mimeType = None
        self.fileName = None

        if isinstance(attachment, tuple):
            self.name = attachment[0]
            self.mimeType = attachment[1]

            f = unQuote(attachment[2])
            p = Path(f)

            try:
                test = p.is_file()
            except OSError:
                self.fileName = None
            else:
                if test:
                    self.fileName = p

        self.span = span
        self.matchString = matchString

    def __str__(self):

        return self.matchString


class MKVAttachments:
    """
     Get attachment files

     Case 1: More than directories with attachments
        Return MKVCommandParser.attachmentsString for every Source

     Case 2: One directory with attachments
        - files in directory differ from total attachments on CL
          return MKVCommandParser.attachmentsString for every Source
        - files in directory equals total attachments on CL
          read directories on parent directory
          * total direcoties equals total source read directories
            and return files read to corresponding source. Directories
            can be empty meaning corresponding source has no attachments.
            This way each source can have different attachment files
          * total directories differ from total source files
            return MKVCommandParser.attachmentsString for every Source
    """

    def __init__(self, strCommand=None):

        # for iterator
        self.__index = 0
        self.strCommand = strCommand

    def _initVars(self):

        self.__attachmentMatch = None
        self.__cmdLineAttachmentsStr = None
        self.__totalSourceFiles = None
        self.__strCommand = None

        self.__attachments = []
        self.__attachmentsFiles = []
        self.__attachmentsDirs = []
        self.__attachmentsStr = []
        self.__attachmentsDirByEpisode = False

        self.__cmdLineAttachments = []
        self.__cmdLineAttachmentsFiles = []
        self.__cmdLineAttachmentsDirs = []

    def __bool__(self):
        return bool(self.__attachments)

    def __contains__(self, item):
        return item in self.__cmdLineAttachments

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.__cmdLineAttachments)

    def __getitem__(self, index):
        return self.__cmdLineAttachments[index]

    def __next__(self):
        if self.__index >= len(self.__cmdLineAttachments):
            self.__index = 0
            raise StopIteration
        else:
            self.__index += 1

    @property
    def attachments(self):
        return self.__attachments

    @property
    def attachmentsDirs(self):
        return self.__attachmentsDirs

    @property
    def isAttachmentsDirByEpisode(self):
        return self.__attachmentsDirByEpisode

    @property
    def attachmentsFiles(self):
        return self.__attachmentsFiles

    @property
    def attachmentsStr(self):
        return self.__attachmentsStr

    @property
    def cmdLineAttachments(self):
        return self.__cmdLineAttachments

    @property
    def cmdLineAttachmentsDirs(self):
        return self.__cmdLineAttachmentsDirs

    @property
    def cmdLineAttachmentsFiles(self):
        return self.__cmdLineAttachmentsFiles

    @property
    def attachmentsMatchString(self):
        strTmp = None
        if self.__cmdLineAttachments:
            span = self.attachmentsSpan
            strTmp = self.strCommand[span[0] : span[1]]
        return strTmp

    @property
    def attachmentsSpan(self):
        span = ()
        if self.__cmdLineAttachments:
            span = (
                self.__cmdLineAttachments[0].span[0],
                self.__cmdLineAttachments[-1].span[1],
            )
        return span

    @property
    def strCommand(self):
        return self.__strCommand

    @strCommand.setter
    def strCommand(self, value):
        if isinstance(value, str):
            self._initVars()
            self.__strCommand = value
            self._parse()
            if self.__cmdLineAttachments:
                self._readDirs()

    def _parse(self):

        reSourceEx = re.compile(r"'\('\s(.*?)\s'\)'")

        reAttachmentsEx = re.compile(
            (
                r"--attachment-name (.*?) --attachment-mime-type "
                r"(.*?) --attach-file (.*?)(?= --)"
            )
        )

        if match := reSourceEx.search(self.__strCommand):

            f = unQuote(match.group(1))
            p = Path(f)

            try:
                test = p.is_file()
            except OSError:
                pass
            else:
                if test:
                    fid = fid = [
                        x for x in p.parent.glob("*" + p.suffix) if x.is_file()
                    ]
                    self.__totalSourceFiles = len(fid)

        if matchAttachments := reAttachmentsEx.finditer(self.__strCommand):
            dirs = set()
            for match in matchAttachments:
                attachment = MKVAttachment(match.groups(), match.span(), match.group())
                self.__cmdLineAttachments.append(attachment)
                p = Path(unQuote(match.group(3)))
                try:
                    test = p.is_file()
                except OSError:
                    pass
                else:
                    if test:
                        self.__cmdLineAttachmentsFiles.append(p)
                        dirs.add(p.parent)
            self.__cmdLineAttachmentsDirs.extend(list(dirs))

    def _readDirs(self):

        if len(self.__cmdLineAttachmentsDirs) == 1:
            # Check parent for directories
            d = self.__cmdLineAttachmentsDirs[0]
            pd = self.__cmdLineAttachmentsDirs[0].parent
            did = [x for x in pd.glob("*") if x.is_dir()]
            fid = [x for x in d.glob("*") if x.is_file()]

            if self.__totalSourceFiles == len(did):
                self.__attachmentsDirByEpisode = True
                self.__attachmentsDirs.extend(did)
                for d in did:
                    fid = [x for x in d.glob("*") if x.is_file()]
                    lstTmp = []
                    lstTmp.extend(fid)
                    self.__attachmentsFiles.append(lstTmp)
                    self.__attachmentsStr.append(attachmentsToStr(lstTmp))
            else:
                self.__attachmentsDirs.extend(
                    self.__cmdLineAttachmentsDirs * self.__totalSourceFiles
                )
                self.__attachmentsStr.extend(
                    [self.attachmentsMatchString] * self.__totalSourceFiles
                )

        else:
            self.__attachmentsStr.extend(
                [self.attachmentsMatchString] * self.__totalSourceFiles
            )


def _attachmentToStr(attachFile):

    strTmp = "--attachment-name " + shlex.quote(attachFile.name)
    strTmp += " --attachment-mime-type " + mimeType(attachFile)
    strTmp += " --attach-file " + shlex.quote(str(attachFile))

    return strTmp


def attachmentsToStr(attachFiles):
    """
    attachmentsToStr convert list of attachment files to mkvmerge option

    Args:
        attachFiles (list): list of attachment files

    Returns:
        str: mkvmerge options string
    """

    strTmp = ""
    bFirst = True
    for f in attachFiles:
        if bFirst:
            strTmp = _attachmentToStr(f)
            bFirst = False
        else:
            strTmp += " " + _attachmentToStr(f)

    return strTmp


def mimeType(fileName):
    """
    mimeType return mime type of known files by suffix

    Args:
        fileName (filepath.Path): file Path object

    Returns:
        str: known mime type for file defaults to application/octet-stream
    """

    if fileName.suffix.upper() in [".TTF", ".TTC"]:
        return "application/x-truetype-font"
    elif fileName.suffix.upper() in [".OTF"]:
        return "application/vnd.ms-opentype"
    elif fileName.suffix.upper() in [".ZIP"]:
        return "application/zip"
    elif fileName.suffix.upper() in [".JPG", ".JPEG"]:
        return "image/jpeg"
    elif fileName.suffix.upper() in [".PNG"]:
        return "image/png"

    return "application/octet-stream"
