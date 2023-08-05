"""
class emit signal that can be received by many Slots
"""

from PySide2.QtCore import QObject, Signal

class QGroupSignal(QObject):
    """
    SetLanguage class to save and trigger multiple slots

    Args:
        QObject (QObject): base class in order to work with Signals
    """

    groupSignal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent
        self.functionSlots = []

    def addSlot(self, function):

        self.groupSignal.connect(function)
        self.functionSlots.append(function)

    def emitSignal(self):

        self.groupSignal.emit()
