"""
 QFrame Lines for separators
"""

from PySide2.QtWidgets import QFrame

class HorizontalLine(QFrame):
    def __init__(self, parent=None, width=1):
        super().__init__(parent)

        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(width)

class VerticalLine(QFrame):
    def __init__(self, parent=None, width=1):
        super().__init__(parent)

        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(width)
