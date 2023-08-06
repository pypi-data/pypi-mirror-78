# PyQt5 Video player
#!/usr/bin/env python

import argparse
import logging
from datetime import datetime, timedelta
import time

__version_info__ = ('0', '0', '11')
__version__ = '.'.join(__version_info__)

from src.VideoTrackingWindow import Ui_VideoTrackingWindow
from src.QVideoWidgetRect import QVideoWidgetRect
from libs.canvas import Canvas
from libs.hashableQListWidgetItem import HashableQListWidgetItem
from libs.shape import Shape

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QDir, Qt, QUrl, pyqtSignal, QPoint, QRect, QObject
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QVideoFrame, QAbstractVideoSurface, QAbstractVideoBuffer, QVideoSurfaceFormat, QVideoProbe
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget,
                             QMainWindow, QPushButton, QAction, QListWidget, QListWidgetItem)
from PyQt5.QtGui import QIcon, QPainter, QImage, QPen, QPixmap, QColor
import sys
import os
import os.path as osp
import numpy as np
import cv2

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *


class VideoSurfaceRects(QAbstractVideoSurface):
    frameAvailable = pyqtSignal(QImage)

    def __init__(self, widget: QWidget, parent: QObject):
        super().__init__(parent)
        self.widget = widget

    def supportedPixelFormats(self, handleType):
        return [QVideoFrame.Format_ARGB32, QVideoFrame.Format_ARGB32_Premultiplied,
                QVideoFrame.Format_RGB32, QVideoFrame.Format_RGB24, QVideoFrame.Format_RGB565,
                QVideoFrame.Format_RGB555, QVideoFrame.Format_ARGB8565_Premultiplied,
                QVideoFrame.Format_BGRA32, QVideoFrame.Format_BGRA32_Premultiplied, QVideoFrame.Format_BGR32,
                QVideoFrame.Format_BGR24, QVideoFrame.Format_BGR565, QVideoFrame.Format_BGR555,
                QVideoFrame.Format_BGRA5658_Premultiplied, QVideoFrame.Format_AYUV444,
                QVideoFrame.Format_AYUV444_Premultiplied, QVideoFrame.Format_YUV444,
                QVideoFrame.Format_YUV420P, QVideoFrame.Format_YV12, QVideoFrame.Format_UYVY,
                QVideoFrame.Format_YUYV, QVideoFrame.Format_NV12, QVideoFrame.Format_NV21,
                QVideoFrame.Format_IMC1, QVideoFrame.Format_IMC2, QVideoFrame.Format_IMC3,
                QVideoFrame.Format_IMC4, QVideoFrame.Format_Y8, QVideoFrame.Format_Y16,
                QVideoFrame.Format_Jpeg, QVideoFrame.Format_CameraRaw, QVideoFrame.Format_AdobeDng]

    def present(self, frame):
        frame = frame.image()
        self.widget.loadPixmap(QPixmap.fromImage(frame))
        self.frameAvailable.emit(frame)

        return True


class VideoTrackingWindow(QMainWindow, Ui_VideoTrackingWindow):

    rectAvailable = pyqtSignal()

    def __init__(self, parent=None):
        super(VideoTrackingWindow, self).__init__(parent)
        # Load UI
        self.setupUi(self)
        # uic.loadUi('VideoTrackingWindow.ui', self)
        self.filePath = None

        self.canvas = Canvas(parent=self)
        self.scrollArea.setWidget(self.canvas)
        self.canvas.scrollRequest.connect(self.scrollRequest)
        self.canvas.newShape.connect(self.newShape)
        self.canvas.shapeMoved.connect(self.shapeMoved)
        self.canvas.selectionChanged.connect(self.shapeSelectionChanged)

        # self.canvas.zoomRequest.connect(self.zoomNavig.zoomRequest)
        self.previous_shape = []

        self.scrollBars = {
            Qt.Vertical: self.scrollArea.verticalScrollBar(),
            Qt.Horizontal: self.scrollArea.horizontalScrollBar()
        }

        # setup media player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoProbe = QVideoProbe()
        # self.videoFrame = QVideoFrame()

        #set Icon for buttons
        self.playButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))
        self.nextButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.prevButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.fastButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.slowButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSeekBackward))

        # setup connection
        self.playButton.clicked.connect(self.playPause)
        self.nextButton.clicked.connect(self.nextFrame)
        self.prevButton.clicked.connect(self.prevFrame)
        self.fastButton.clicked.connect(self.fastPlayback)
        self.slowButton.clicked.connect(self.slowPlayback)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.actionOpen_Video.triggered.connect(self.openVideo)
        self.actionSave_Annotation.triggered.connect(self.saveAnnotations)
        self.actionExit.triggered.connect(self.exitCall)

        # Setup the Media Player
        self.videoSurface = VideoSurfaceRects(self.canvas, self)
        self.mediaPlayer.setVideoOutput(self.videoSurface)
        self.videoSurface.frameAvailable.connect(self.processFrame)

        self.videoProbe.setSource(self.mediaPlayer)
        # self.videoProbe.videoFrameProbed.connect(self.processFrame)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        # Set Tracking
        # self.listTracker=[]
        self.removeTracker.clicked.connect(self.removeTrackerClicked)
        self.addTracker.clicked.connect(self.addTrackerClicked)
        self.stopTracker.clicked.connect(self.stopTrackerClicked)
        # self.runTracker.clicked.connect(self.runTrackerClicked)
        self.FPS = 30

        # self.rectAvailconnect

        # print("set rectangle color and thickness")
        self.penRectangle = QPen(QtCore.Qt.red)
        self.penRectangle.setWidth(10)
        self.painterInstance = QPainter()

        self._noSelectionSlot = False
        self.itemsToShapes = {}
        self.shapesToItems = {}

        # self.tracking = False
        self.logging("Application initialized")

        self.playtracking = False

        self.prevPosition = 0

        self.frame2pos = []

    @property
    def DeltaT(self):
        return 1000/self.FPS

    def playPause(self):
        if self.isTracking():
            self.playtracking = not self.playtracking
            if self.playtracking:
                self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
                self.nextFrame()

                # self.mediaPlayer.setPosition(
                #     int(self.mediaPlayer.position()+self.DeltaT))
            else:
                self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.mediaPlayer.pause()
            else:
                self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        if self.isTracking(self.prevPosition) != self.isTracking(position):
            # print("hello!")
            # if self.isTracking(position):
            if self.playtracking:
                self.playtracking = False
                self.logging(
                    f"Paused at time: {self.mediaPlayer.position()/1000:.3f} s [End of Tracking]")
            # else:
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.mediaPlayer.pause()
                self.logging(
                    f"Paused at time: {self.mediaPlayer.position()/1000:.3f} s [Start of Tracking]")

            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
            # return
        self.positionSlider.setValue(position)
        self.checkIfTracking.setChecked(self.isTracking())
        # self.centralwidget.setEnabled(not self.isTracking())
        # self.tabWidget.setCurrentIndex(int(self.isTracking()))
        strPosition = str(timedelta(seconds=int(
            self.mediaPlayer.position()/1000)))
        strDuration = str(timedelta(seconds=int(
            self.mediaPlayer.duration()/1000)))
        self.timeLabel.setText(f"{strPosition}/{strDuration}")
        self.prevPosition = position

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        # self.positionSlider.setTickInterval(1000)

        self.frame2pos = [0]
        t = 0
        while t < duration:
            t += self.DeltaT
            self.frame2pos.append(int(t))

    def setPosition(self, position):
        self.previous_shape = self.canvas.shapes

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        self.mediaPlayer.setPosition(int(position/self.DeltaT)*self.DeltaT)
        self.logging(
            f"Position set at time: {self.mediaPlayer.position()/1000:.3f} s")
        # print("pos in frame?", self.mediaPlayer.position() in self.frame2pos)

    def nextFrame(self):
        self.setPosition(
            int(self.mediaPlayer.position()+self.DeltaT*1.5))

    def prevFrame(self):

        self.setPosition(
            int(self.mediaPlayer.position()-self.DeltaT))

    def fastPlayback(self):
        self.mediaPlayer.setPlaybackRate(self.mediaPlayer.playbackRate()*2.0)
        self.logging(
            f"Playback speed set to {self.mediaPlayer.playbackRate()}x")

    def slowPlayback(self):
        self.mediaPlayer.setPlaybackRate(self.mediaPlayer.playbackRate()/2.0)
        self.logging(
            f"Playback speed set to {self.mediaPlayer.playbackRate()}x")

    def handleError(self):
        self.centralwidget.setEnabled(False)
        self.logging("Error: " + self.mediaPlayer.errorString())

    def logging(self, message):
        logging.info(message)
        self.statusBar.showMessage(message)

    def openVideo(self, filename=False):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, "Open Video",
                                                      QDir.homePath())
        self.path = osp.dirname(str(filename))
        if filename != '':
            self.filename = filename
            # read FPS
            cap = cv2.VideoCapture(filename)
            self.FPS = cap.get(cv2.CAP_PROP_FPS)
            self.logging(f"FPS read: {self.FPS} fps")
            # read Media
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(filename)))
            self.centralwidget.setEnabled(True)
            self.logging(f"Video {filename} opened")

            # self.mediaPlayer.play()
            self.mediaPlayer.pause()

    def saveAnnotations(self, filename=False):
        filename = os.path.splitext(self.filename)[0]+".txt"

        # if not filename:
        #     filename, _ = QFileDialog.getOpenFileName(self, "Where to save",
        #                                               QDir.homePath())

        if filename == '':
            self.logging("Please select a path to save the annotations")
            return
        with open(filename, "w") as file_object:

            for i in range(self.listTracker.count()):
                this_item = self.listTracker.item(i)
                this_tracker = self.listTracker.itemWidget(this_item)
                # this_tracker.boxes
                for pos, box, _ in this_tracker:
                    lineBB = f"{int(pos):016d}, {box.x()}, {box.y()}, {box.width()}, {box.height()} \n"
                    print(lineBB)
                    file_object.write(lineBB)

    def exitCall(self):
        self.logging("Exiting the application")
        sys.exit(app.exec_())

    def shapeMoved(self):
        self.previous_shape = self.canvas.shapes
        for shape in self.canvas.shapes:
            item = self.shapesToItems[shape]
            tracker = self.listTracker.itemWidget(item)
            tracker.resetTracker(new_state=tuple(shape2box(shape)))

    def isTracking(self, pos=None):
        # print("isTracking?")
        if pos is None:
            pos = self.mediaPlayer.position()

        for i in range(self.listTracker.count()):
            this_item = self.listTracker.item(i)
            this_tracker = self.listTracker.itemWidget(this_item)
            if this_tracker.isTracking(pos):
                return True
        return False

    def processFrame(self, videoFrame):
        currentPos = self.mediaPlayer.position()

        self.canvas.shapes

        self.qimage = videoFrame.convertToFormat(4)
        if self.qimage.bits() is None:
            return

        new_shapes = []

        # List shape already drawn previously
        for i in range(self.listTracker.count()):
            this_item = self.listTracker.item(i)
            this_tracker = self.listTracker.itemWidget(this_item)
            if currentPos in this_tracker.times:
                new_box = this_tracker.boxes[this_tracker.times.index(
                    currentPos)]
                new_shape = Shape(label="Tracker")
                new_shape.addPoint(new_box.topLeft())
                new_shape.addPoint(new_box.topRight())
                new_shape.addPoint(new_box.bottomRight())
                new_shape.addPoint(new_box.bottomLeft())
                new_shapes.append(new_shape)

                self.itemsToShapes[this_item] = new_shape
                self.shapesToItems[new_shape] = this_item

        # List shape from previous canvas, for tracking
        for shape in self.previous_shape:
            this_item = self.shapesToItems[shape]
            this_tracker = self.listTracker.itemWidget(this_item)
            if this_tracker.isTracking(currentPos):
                # self.surface
                if currentPos in this_tracker.times:
                    print("already tracked!")
                    continue

                new_box = this_tracker.run(self.qimage, currentPos)

                if new_box.topLeft == new_box.bottomRight:
                    # self.listTracker.repaint()
                    self.playtracking = False
                    # self.SP_MediaPlay.

                    self.playButton.setIcon(
                        self.style().standardIcon(QStyle.SP_MediaPlay))
                    continue

                print(new_box)
                new_shape = Shape(label="Tracker")
                new_shape.addPoint(new_box.topLeft())
                new_shape.addPoint(new_box.topRight())
                new_shape.addPoint(new_box.bottomRight())
                new_shape.addPoint(new_box.bottomLeft())
                print(new_shape)

                # print(self.canvas.shapes)
                new_shapes.append(new_shape)
                # print(self.canvas.shapes)

                self.itemsToShapes[this_item] = new_shape
                self.shapesToItems[new_shape] = this_item
                # self.videoWidget.rects.append(new_box)
        # self.videoWidget.repaint()
        # self.showThumbNail()

        self.canvas.shapes = new_shapes
        self.canvas.repaint()
        if self.playtracking and self.isTracking():
            self.nextFrame()
            # self.mediaPlayer.setPosition(
            #     int(self.mediaPlayer.position()+self.DeltaT))

    def stopTrackerClicked(self):

        current_item = self.listTracker.currentItem()
        current_tracker = self.listTracker.itemWidget(current_item)
        if current_tracker.isTracking(self.mediaPlayer.position()):
            current_tracker.time_stop = self.mediaPlayer.position()
            current_tracker.updateItem()
            # self.centralwidget.setEnabled(not self.isTracking())
            # self.tabWidget.setCurrentIndex(int(self.isTracking()))
            self.positionChanged(self.mediaPlayer.position())
        else:
            self.logging("Tracker already done")

        # self.videoWidget.clearRectangles()
        self.stopTracker.setEnabled(self.listTracker.count() > 0)

    def removeTrackerClicked(self):
        current_item = self.listTracker.currentItem()
        current_shape = self.itemsToShapes[current_item]
        if current_shape in self.canvas.shapes:
            self.canvas.shapes.remove(current_shape)

        self.canvas.repaint()
        self.listTracker.takeItem(self.listTracker.row(current_item))

        # current_tracker = self.listTracker.itemWidget(current_item)

    def addTrackerClicked(self):
        self.mediaPlayer.pause()
        self.canvas.setEditing(False)

    def shapeSelectionChanged(self, selected=False):
        if self._noSelectionSlot:
            self._noSelectionSlot = False
        else:
            shape = self.canvas.selectedShape
            if shape:
                self.shapesToItems[shape].setSelected(True)
            # else:
            #     self.labelList.clearSelection()
        # self.deleteAction.setEnabled(selected)

    def scrollRequest(self, delta, orientation):
        units = - delta / (8 * 15)
        bar = self.scrollBars[orientation]
        bar.setValue(bar.value() + bar.singleStep() * units)

    def newShape(self):
        """Pop-up and give focus to the label editor.
        position MUST be in global coordinates.
        """
        print("newShape")
        self.canvas.setEditing(True)
        shape = self.canvas.setLastLabel("Tracker")
        print(shape)
        print(shape.points)

        # item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        # item.setCheckState(Qt.Checked)
        # item.setBackground(generateColorByText(shape.label))
        # self.itemsToShapes[item] = shape
        # self.shapesToItems[shape] = item

        # qimage = self.videoSurface.videoFrame_QImage.convertToFormat(4)
        ptr = self.qimage.bits()
        ptr.setsize(self.qimage.byteCount())
        img = np.array(ptr).reshape(
            self.qimage.height(), self.qimage.width(), 4)  # Copies the data

        # display_name = f'Display: Draw Initial Bounding Box'
        # cv2.imshow(display_name, img)
        # valid_selection = False
        # init_state = [0, 0, 0, 0]

        # while not valid_selection:
        #     frame_disp = img.copy()

        #     cv2.putText(frame_disp, 'Select target ROI and press ENTER [ESC to use previous BB]', (20, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
        #                 1.5, (0, 0, 0), 1)

        #     x, y, w, h = cv2.selectROI(
        #         display_name, frame_disp, fromCenter=False)
        #     init_state = [x, y, w, h]
        #     valid_selection = np.sum(init_state)
        #     if cv2.waitKey(0) == 27:
        #         cv2.destroyAllWindows()
        #         break
        # cv2.destroyAllWindows()
        # print("annot", init_state)

        # # print(self.grabber.rects)
        init_state = shape2box(shape)
        new_tracker = Tracker(time_start=self.mediaPlayer.position(),
                              time_stop=self.mediaPlayer.duration(),
                              init_QImage=self.qimage,
                              init_box=init_state,
                              FPS=self.FPS)

        # # self.videoWidget.rects.append(new_tracker.box2rect(init_state))
        # self.videoWidget.rects.append(new_tracker.box2rect(init_state))
        # # self.rectAvailable.emit()
        # self.videoWidget.repaint()

        item = HashableQListWidgetItem(self.listTracker)
        item.setSizeHint(new_tracker.minimumSizeHint())

        self.listTracker.addItem(item)

        self.listTracker.setItemWidget(item, new_tracker)
        self.listTracker.setCurrentItem(item)

        self.itemsToShapes[item] = shape
        self.shapesToItems[shape] = item

        self.stopTracker.setEnabled(self.listTracker.count() > 0)
        # print(self.isTracking())


def box2shape(box, label):
    shape = Shape(label=label)
    shape.addPoint(QPointF(box[0], box[1]))
    shape.addPoint(QPointF(box[0], box[1]+box[3]))
    shape.addPoint(QPointF(box[0]+box[2], box[1]+box[3]))
    shape.addPoint(QPointF(box[0]+box[2], box[1]))
    return shape


def shape2box(shape):
    shape_xmax = 0
    shape_xmin = 99999
    shape_ymax = 0
    shape_ymin = 99999
    for p in shape.points:
        if shape_xmax < p.x():
            shape_xmax = p.x()
        if shape_ymax < p.y():
            shape_ymax = p.y()
        if shape_xmin > p.x():
            shape_xmin = p.x()
        if shape_ymin > p.y():
            shape_ymin = p.y()
    return [shape_xmin, shape_ymin, shape_xmax - shape_xmin, shape_ymax - shape_ymin]
# def cropQImage()


OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}


class Tracker(QWidget):
    def __init__(self, time_start, time_stop, init_box, init_QImage, FPS, parent=None):
        super(Tracker, self).__init__(parent)
        self.time_start = time_start
        # print(time_start)
        self.time_stop = time_stop
        # print(time_stop)
        self.FPS = FPS
        self.trackingAlgorithm = None
        # self.boxes = {f"{self.time_start}": self.box2rect(init_box)}
        # self.frames = {f"{self.time_start}": init_QImage}

        self.boxes = [self.box2rect(init_box)]
        self.frames = [self.QImage2CVImage(init_QImage)]
        self.times = [self.time_start]

        pixmap = QPixmap.fromImage(init_QImage)
        pixmap = pixmap.copy(self.boxes[-1])
        pixmap = pixmap.scaled(20, 20, QtCore.Qt.KeepAspectRatio)
        self.iconQLabel = QLabel()
        self.iconQLabel.setPixmap(pixmap)

        self.nameQLabel = QLabel()
        self.nameQLabel.setText(self.getName())

        self.row = QHBoxLayout()
        self.row.addWidget(self.iconQLabel)
        self.row.addWidget(self.nameQLabel)
        self.setLayout(self.row)

        self.tracker = OPENCV_OBJECT_TRACKERS["kcf"]()

        # self.image = QVideoFrame(self.videoFrame).image().convertToFormat(4)
        # ret = self.image.save(f'frame_pos{self.mediaPlayer.position()}.jpg')

        # cv2.imwrite(f'framecv_pos{self.time_start}.jpg', CVImage)
        # print(tuple(init_box))
        self.tracker.init(self.frames[0], tuple(init_box))

    def QImage2CVImage(self, myQimg):
        ptr = myQimg.bits()
        ptr.setsize(myQimg.byteCount())
        return np.array(ptr).reshape(myQimg.height(), myQimg.width(), 4)

    def resetTracker(self, new_state):
        self.tracker.clear()
        self.tracker = OPENCV_OBJECT_TRACKERS["kcf"]()
        self.tracker.init(self.frames[-1], new_state)

    def run(self, qimage, pos):
        # print("self.qimage is none", qimage)
        # if qimage is None:
        #     print("self.qimage is none", qimage)
        #     return self.box2rect((0.0,0.0,0.0,0.0))
        img = self.QImage2CVImage(qimage)[:, :, :3]
        # ptr = qimage.bits()
        # ptr.setsize(qimage.byteCount())
        # img = np.array(ptr).reshape(
        #     qimage.height(), qimage.width(), 4)  # Copies the data
        # img = img[:, :, :3]
        # print(img.shape)
        # cv2.imwrite(f'framecv_pos{currentPos}.jpg', img)
        # tries = 0
        # success=False
        # while tries < 3 and not success:
        (success, box) = self.tracker.update(img)
        print("success", success, box)
        # tries += 1

        if not success:
            # self.trackingLost.emit()
            self.time_stop = self.times[-1]  # ? pax

            self.updateItem()
            return self.box2rect(box)

        # new_frame = qimage.copy()
        # QRect(this_tracker.boxes[str(previousPos)])
        # new_box = QRect(self.box2rect(box))

        # this_tracker.boxes[str(currentPos)] = new_box
        # this_tracker.frames[str(currentPos)] = new_frame
        # if pos is None:
        #     pos = int(self.times[-1]+self.DeltaT)

        self.times.append(pos)
        self.frames.append(img)
        self.boxes.append(self.box2rect(box))
        return self.boxes[-1]

    def get_Rect(self, time):
        print("getRect", self.times, time)
        try:
            i = self.times.index(time)
        except ValueError:
            return None
        print(i)

        return self.boxes[i]

    @property
    def DeltaT(self):
        return 1000/self.FPS

    def __getitem__(self, i):
        # key = int(self.time_start + i*self.DeltaT)
        # box = self.boxes[key]
        # frame = self.frames[key]
        return self.times[i], self.boxes[i], self.frames[i]

    def isTracking(self, pos):
        return not self.afterTracking(pos) and not self.beforeTracking(pos)

    def afterTracking(self, pos):
        return pos >= self.time_stop

    def beforeTracking(self, pos):
        return pos < self.time_start

    def updateItem(self):
        self.nameQLabel.setText(self.getName())

    def box2rect(self, box):
        return QRect(box[0], box[1], box[2], box[3])

    def rect2box(self, rect):
        return (rect.x(), rect.y(), rect.width(), rect.height())

    def printRect(self, rect):
        return f"X:{rect.center().x()}/Y:{rect.center().y()}"

    def getName(self):
        return f"From {self.time_start/1000}s to {self.time_stop/1000}s"

    def addBox(self, box):
        self.boxes.append(box)


def main():
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser(
        description="Image Labeler based on Active Learning")

    parser.add_argument("--videopath",
                        default=None,
                        type=str,
                        help="video to open")

    parser.add_argument("--logdir",
                        default="log",
                        type=str,
                        help="diretory for logging")

    parser.add_argument("--loglevel",
                        default="INFO",
                        type=str,
                        help="diretory for logging")
    args = parser.parse_args()

    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel)

    # set up logging configuration
    log_file = os.path.join(
        args.logdir, datetime.now().strftime('%Y-%m-%d %H-%M-%S.log'))
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        level=numeric_level,  # INFO
        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        handlers=[
            # file handler
            logging.FileHandler(log_file),
            # stream handler
            logging.StreamHandler()
        ])
    logging.info(f"Start logging on {log_file}")
    logging.info(f"Starting Videotracking version {__version__}")

    player = VideoTrackingWindow()
    player.resize(720, 480)
    player.showMaximized()

    if args.videopath is not None:
        player.openVideo(filename=args.videopath)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
