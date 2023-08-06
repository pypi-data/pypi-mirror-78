"""
OutputTextWidget:

Output widget form just to output text in color

"""
# OTW0004 Next log ID

import logging


from PySide2.QtCore import Qt, Signal, Slot
from PySide2.QtGui import QTextCursor
from PySide2.QtWidgets import QTextEdit


from .insertTextHelpers import checkColor, LineOutput


MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class QOutputTextWidget(QTextEdit):
    """Output for running queue"""

    # log state
    __log = False
    clearSignal = Signal()
    insertTextSignal = Signal(str, dict)
    setCurrentIndexSignal = Signal()
    isDarkMode = False

    def __init__(self, parent=None, log=None, **kwargs):
        super().__init__(parent=parent, **kwargs)

        self.parent = parent
        self.__log = None
        self.__tab = None
        self.__tabWidget = None
        self.log = log

        self.insertTextSignal.connect(self.insertText)
        self.clearSignal.connect(super().clear)

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

        return QOutputTextWidget.classLog()

    @log.setter
    def log(self, value):
        """set instance log variable"""
        if isinstance(value, bool) or value is None:
            self.__log = value

    def connectToInsertText(self, objSignal):
        """Connect to signal"""

        objSignal.connect(self.insertText)

    @Slot(str, dict)
    def insertText(self, strText, kwargs):
        """
        insertText - Insert text in output window.
        Cannot use standard keyword arguments on
        emit calls using a dictionary argument instead

        Args:
            strText (str): text to insert on output window
            kwargs (dict): additional arguments in dictionary
                           used like **kwargs
        """

        strTmp = ""

        color = kwargs.pop(LineOutput.Color, None)
        replaceLine = kwargs.pop(LineOutput.ReplaceLine, False)
        appendLine = kwargs.pop(LineOutput.AppendLine, False)
        appendEnd = kwargs.pop(LineOutput.AppendEnd, False)
        logOnly = kwargs.pop(LineOutput.LogOnly, False)
        overrideLog = kwargs.pop("log", None)

        # still no restore to default the ideal configuration
        # search will continue considering abandoning color

        if not logOnly:
            color = checkColor(color, QOutputTextWidget.isDarkMode)

            if replaceLine:
                self.moveCursor(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
            elif appendEnd:
                self.moveCursor(QTextCursor.End)

            if color is not None:
                self.setTextColor(color)

            if replaceLine:
                self.insertPlainText(strText)
            elif appendLine:
                self.append(strText)
            elif appendEnd:
                self.append(strText)
            else:
                self.insertPlainText(strText)

            self.ensureCursorVisible()

        log = self.log

        if overrideLog is not None:
            log = overrideLog

        if log or logOnly:
            strTmp = strTmp + strText
            strTmp = strTmp.replace("\n", " ")

            if strTmp != "" and strTmp.find(u"Progress:") != 0:
                if strTmp.find(u"Warning") == 0:
                    MODULELOG.warning("OTW0001: %s", strTmp)
                elif strTmp.find(u"Error") == 0 or color == Qt.red:
                    MODULELOG.error("OTW0002: %s", strTmp)
                else:
                    if strTmp.strip():
                        MODULELOG.debug("OTW0003: %s", strTmp)
