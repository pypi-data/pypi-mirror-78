""" QLogHandler """

import logging

from PySide2.QtCore import QObject, Signal


class Communicate(QObject):
    logRecord = Signal(object)


class QSignalLogHandler(logging.Handler):

    """
    logging handler that rotate files at initialization time
    this will create a new file each time is run against
    the same log file.

    Args:
        **kwargs: variable number of key value parameters
            that are passed to the super class on
            initialization
    """

    def __init__(self, slotFunction=None, **kwargs):
        super().__init__(**kwargs)

        self.signal = Communicate()

        if slotFunction is not None:
            self.connect(slotFunction)

    def emit(self, record):
        msg = self.format(record)
        self.signal.logRecord.emit(msg)

    def connect(self, slotFunction):

        self.signal.logRecord.connect(slotFunction)
