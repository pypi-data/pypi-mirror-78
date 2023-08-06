

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import QPen
from PyQt5 import QtCore

class QVideoWidgetRect(QWidget):

    def __init__(self, parent=None):
        super(QVideoWidgetRect, self).__init__(parent)
        self.videoFrame_PixMap = None
        self.rects = []

        self.penRectangle = QPen(QtCore.Qt.red)
        self.penRectangle.setWidth(10)
        # self.painterInstance = QPainter()

    def paintEvent(self, paintEvent):
        print("QVideoWidgetRect paintEvent")
        super(QVideoWidgetRect, self).paintEvent(paintEvent)
        
        if self.videoFrame_PixMap is not None:
            # create Painter
            painter = QPainter(self)

            p2 = QPainter(self.videoFrame_PixMap)
            # Draw Rectangles
            p2.setPen(self.penRectangle)
            for rect in self.rects:
                p2.drawRect(rect)
            # painter.end()


            # draw Frame
            painter.drawPixmap(self.rect(), self.videoFrame_PixMap)
            # painter.begin(self.videoFrame_PixMap)


    def setPixmap(self, pix):
        self.videoFrame_PixMap = pix

    def clearRectangles(self):
        self.rects = []

    def addRectangle(self, rect):
        self.rects.append(rect)

    def addRectangles(self, rects):
        for rect in rects:
            self.addRectangle(rect)
        

