"""
Get file structure information from media file
"""

# MFI0001

import base64
import logging

from pymediainfo import MediaInfo

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class MediaFileInfo(object):
    """
    Media file properties
    This class main function is to verify that the structure of the files
    is the same:

        Same order of tracks
        Same language if it applies

    Args:

        strMediaFile (str): name with fullpath of source file

    Attributes:

        lstMediaTracks (MediaTrackInfo): list of media tracks
            found
    """

    # log state
    __log = False

    @classmethod
    def classLog(cls, setLogging=None):
        """
        get/set logging at class level
        every class instance will log
        unless overwritten

        Args:
            setLogging (bool):
                - True class will log
                - False turn off logging
                - None returns current Value

        Returns:
            bool:

            returns the current value set
        """

        if setLogging is not None:
            if isinstance(setLogging, bool):
                cls.__log = setLogging

        return cls.__log

    def __init__(self, strMediaFile, log=None):

        self.fileName = strMediaFile
        self.mediaInfo = None
        self.codec = ""
        self.format = ""
        self.title = ""
        self.lstMediaTracks = []
        self.__log = None
        self.log = log
        self.totalTracks = {"Video": 0, "Audio": 0, "Text": 0}
        self._initHelper()

    def _initHelper(self):

        try:
            fileMediaInfo = MediaInfo.parse(self.fileName)
            self.mediaInfo = fileMediaInfo
        except OSError:
            raise OSError("MediaInfo not found.")

        for track in fileMediaInfo.tracks:
            if track.track_type == "General":
                self.codec = track.codec
                self.format = track.format
                if track.title is not None:
                    self.title = track.title
                    try:
                        self.title = base64.b64decode(track.title).decode("UTF-8")
                    except: # pylint: disable=bare-except
                        pass
                    self.title = self.title.strip()
            if track.track_type in ("Video", "Audio", "Text"):
                self.totalTracks[track.track_type] += 1
                self.lstMediaTracks.append(
                    MediaTrackInfo(track.streamorder, track.track_type,
                                   track.language, track.default, track.forced,
                                   track.title, track.codec, track.format))
    def __len__(self):
        return len(self.lstMediaTracks) if self.lstMediaTracks else 0

    def __eq__(self, objOther):

        bReturn = True

        if self.log:
            MODULELOG.debug(
                "MFI0001: Structure equality test between [%s] and [%s]",
                self.fileName, objOther.fileName)
            MODULELOG.debug("MFI0002: FORMAT: %s", self.format)

        if self.codec != objOther.codec:
            if self.log:
                MODULELOG.debug("MFI0003: Codec mismatched %s - %s", self.codec,
                                objOther.codec)
            bReturn = False
        elif len(self) != len(objOther):
            if self.log:
                MODULELOG.debug("MFI0004: Number of tracks mismatched %s - %s",
                                len(self), len(objOther))
            bReturn = False
        elif len(self) == len(objOther):
            for a, b in zip(self.lstMediaTracks, objOther.lstMediaTracks):
                if a.streamorder != b.streamorder:
                    if self.log:
                        MODULELOG.debug(
                            "MFI0005:  Stream order mismatched %s - %s",
                            a.streamorder, b.streamorder)
                    bReturn = False
                elif a.track_type != b.track_type:
                    if self.log:
                        MODULELOG.debug(
                            "MFI006: Stream type mismatched %s - %s",
                            a.track_type, b.track_type)
                    bReturn = False
                elif (a.language != b.language) and (a.track_type != "Video"):
                    if self.log:
                        MODULELOG.debug(
                            "MFI0007: Stream language mismatched %s - %s",
                            a.language, b.language)
                    if self.format == 'AVI':
                        # Ignore language for AVI container
                        if self.log:
                            MODULELOG.debug(
                                "MFI0008: AVI container ignore language mismatched %s - %s",
                                a.track_type, b.track_type)
                    else:
                        bReturn = False
                elif (a.codec != b.codec) and (a.track_type != "Audio"):
                    if self.log:
                        MODULELOG.debug("MFI0009: Codec mismatched %s - %s",
                                        a.codec, b.codec)
                    if self.format == 'AVI':
                        # Ignore language for AVI container
                        if self.log:
                            MODULELOG.debug(
                                "MFI0010: AVI container ignore codec mismatched %s - %s",
                                a.codec, b.codec)
                    else:
                        bReturn = False
                elif a.format != b.format:
                    if self.log:
                        MODULELOG.debug(
                            "MFI0011: Stream format mismatched %s - %s",
                            a.format, b.format)
                    bReturn = False

        if self.log:
            if bReturn:
                MODULELOG.debug("MFI0012: Structure found ok.", )
            else:
                MODULELOG.debug("MFI0013: Structure not ok.", )

        return bReturn

    def __str__(self):

        tmpStr = "File Name: {}\nFile Format: -{}-\n\n".format(
            self.fileName, self.format)
        tmpNum = 1

        for track in self.lstMediaTracks:
            tmpStr += "Track: {}\n".format(tmpNum)
            tmpStr += "Order: {} - {}\n".format(track.streamorder,
                                                track.track_type)
            tmpStr += "Codec: {}\n".format(track.codec)
            tmpStr += "Language: {}\n".format(track.language)
            tmpStr += "Format: {}".format(track.format)
            tmpNum += 1

        return tmpStr

    @property
    def log(self):
        """
        class property can be used to override the class global
        logging setting

        Returns:
            bool:

            True if logging is enable False otherwise
        """
        if self.__log is not None:
            return self.__log

        return MediaFileInfo.classLog()

    @log.setter
    def log(self, value):
        """set instance log variable"""
        if isinstance(value, bool) or value is None:
            self.__log = value


class MediaTrackInfo:
    r"""
    Convenience class used by MediaFileInfo_
    contains the media track properties

    Args:
        streamorder (:obj:`str`, optional): order of track
        track_type (:obj:`str`, optional): type of track
        language (:obj:`str`, optional): language of track
        default (:obj:`str`, optional): is this a default track
        forced (:obj:`str`, optional): is this a forced track
        title (:obj:`str`, optional): title of track
        codec (:obj:`str`, optional): codec used on track
        format\_ (:obj:`str`, optional): format of track

    Attributes:
        streamorder (str): Stream order
        track_type (str): Track Type
        language (str): Language of track
        default (str): Is a default track
            'Yes' it is 'No' otherwise
        forced (str): Is a forced track
            'Yes' it is 'No' otherwise
        title (str): Track tittle
        codec (str): Codec used
        format (str): Track format
    """

    def __init__(self,
                 streamorder=None,
                 track_type=None,
                 language=None,
                 default=None,
                 forced=None,
                 title=None,
                 codec=None,
                 format_=None):

        self.streamorder = streamorder
        self.track_type = track_type  # pylint: disable=C0103
        self.language = language
        self.default = default
        self.forced = forced
        self.title = title
        self.codec = codec
        self.format = format_

    def __str__(self):
        return "Stream Order: " + str(self.streamorder) \
            + "\nTrack Type: " + str(self.track_type) \
            + "\nLanguage: " + str(self.language) \
            + "\nDefault Track : " + str(self.default) \
            + "\nForced Track: " + str(self.forced) \
            + "\nTrack Title: " + str(self.title) \
            + "\nCodec: " + str(self.codec) \
            + "\nFormat: " + str(self.format) \
            + "\n"
