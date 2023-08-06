"""

The MIT License (MIT)

Copyright (c) 2011 Morgan Leborgne

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


QProgressIndicator

Returns:
    [type]: [description]
"""

import sys

from PySide2.QtCore import Qt, QSize, Signal, Slot
from PySide2.QtGui import QPainter, QColor
from PySide2.QtWidgets import QWidget, QApplication, QSizePolicy

from .SvgColor import SvgColor


class QProgressIndicator(QWidget):
    """
    ProgressIndicator show progress animation
    """

    startAnimationSignal = Signal()
    stopAnimationSignal = Signal()


    def __init__(self, parent):
        # Call parent class constructor first
        super(QProgressIndicator, self).__init__(parent)

        # Initialize instance variables
        self.angle = 0
        self.timerId = -1

        self.__delay = 40
        self.__displayedWhenStopped = False
        self.__color = SvgColor.black

        # Set size and focus policy
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFocusPolicy(Qt.NoFocus)

        self.startAnimationSignal.connect(self.startAnimation)
        self.stopAnimationSignal.connect(self.stopAnimation)

        # Show the widget
        self.show()

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value
        self.update()

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, value):
        self.__delay = value
        if self.timerId != -1:
            self.killTimer(self.timerId)
            self.timerId = self.startTimer(self.__delay)

    @property
    def displayedWhenStopped(self):
        return self.__displayedWhenStopped

    @displayedWhenStopped.setter
    def displayedWhenStopped(self, value):
        self.__displayedWhenStopped = value
        self.update()

    def heightForWidth(self, w):
        return w

    def sizeHint(self):
        return QSize(30, 30)

    def timerEvent(self, event):  # pylint: disable=unused-argument
        self.angle = (self.angle + 30) % 360
        self.update()

    def paintEvent(self, event):  # pylint: disable=unused-argument
        if (not self.displayedWhenStopped) and (not self.isAnimated()):
            return

        width = min(self.width(), self.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        outerRadius = (width - 1) * 0.5
        innerRadius = (width - 1) * 0.5 * 0.38

        capsuleHeight = outerRadius - innerRadius
        capsuleWidth = capsuleHeight * 0.23 if (width > 32) else capsuleHeight * 0.35
        capsuleRadius = capsuleWidth / 2

        for i in range(0, 12):
            color = QColor(self.color)

            color.setAlphaF(1.0 - (i / 12.0))

            p.setPen(Qt.NoPen)
            p.setBrush(color)
            p.save()
            p.translate(self.rect().center())
            p.rotate(self.angle - (i * 30.0))
            p.drawRoundedRect(
                -capsuleWidth * 0.5,
                -(innerRadius + capsuleHeight),
                capsuleWidth,
                capsuleHeight,
                capsuleRadius,
                capsuleRadius,
            )
            p.restore()

    def isAnimated(self):
        return self.timerId != -1

    @Slot()
    def startAnimation(self):
        self.angle = 0
        if self.timerId == -1:
            self.timerId = self.startTimer(self.delay)

    @Slot()
    def stopAnimation(self):
        if self.timerId != -1:
            self.killTimer(self.timerId)

        self.angle = 0
        self.timerId = -1
        self.update()


if __name__ == "__main__":

    from PySide2.QtWidgets import QGridLayout, QMainWindow, QPushButton

    class MainWindow(QMainWindow):
        """Test the progress bars"""

        def __init__(self, *args, **kwargs):
            super(MainWindow, self).__init__(*args, **kwargs)

            l = QGridLayout()

            self.pi = QProgressIndicator(self)
            self.pi.displayedWhenStopped = True

            a = QPushButton("Animate")
            a.pressed.connect(self.animate)
            s = QPushButton("Stop Animation")
            s.pressed.connect(self.stopAnimation)

            l.addWidget(self.pi, 0, 0, Qt.AlignCenter)
            l.addWidget(a, 1, 0)
            l.addWidget(s, 2, 0)

            w = QWidget()
            w.setLayout(l)

            self.setCentralWidget(w)

            self.show()

        def animate(self):
            self.pi.startAnimation()

        def stopAnimation(self):
            self.pi.stopAnimation()

    # pylint: disable=invalid-name
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
