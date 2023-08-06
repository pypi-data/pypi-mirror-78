# PyQt5 Video player
#!/usr/bin/env python

from libs.zoomWidget import ZoomWidget
import argparse
import logging
from datetime import datetime, timedelta
import time

__version_info__ = ('0', '0', '16')
__version__ = '.'.join(__version_info__)

from src.VideoTrackingWindow import Ui_VideoTrackingWindow
from libs.canvas import Canvas
from libs.hashableQListWidgetItem import HashableQListWidgetItem
from libs.shape import Shape
from libs.utils import *

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
import skvideo
import skvideo.io

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

# background Thread for reading video frames


class ProcessRunnable(QRunnable):
    def __init__(self, target, args):
        QRunnable.__init__(self)
        self.t = target
        self.args = args

    def run(self):
        self.t(*self.args)

    def start(self):
        QThreadPool.globalInstance().start(self)


def runReadVideo(parent, videogen, fps_real=None, fps_desired=None, height=None, width=None, function="appendFrame"):
    # loop over videogen that yield opencv-friendly frames

    drop_extra_frames = fps_real/fps_desired

    for i, frame in enumerate(videogen):

        if i % drop_extra_frames < 1:  # desired FPS
            # if int(i % drop_every_X) < drop_every_X

            frame = cv2.resize(frame, (height, width))

            # convert opencv frames into QImages
            h, w, ch = frame.shape  # get shape
            bytesPerLine = ch * w  # get bute per lines
            qImage = QImage(frame.data, w, h, bytesPerLine,
                            QImage.Format_RGB888)  # create QImage
            QMetaObject.invokeMethod(
                parent, function, Qt.QueuedConnection, Q_ARG(QImage, qImage))


class VideoTrackingWindow(QMainWindow, Ui_VideoTrackingWindow):

    changePixmapIndex = pyqtSignal(int)

    def __init__(self, parent=None):
        super(VideoTrackingWindow, self).__init__(parent)
        # Load UI
        self.setupUi(self)
        # uic.loadUi('VideoTrackingWindow.ui', self)
        self.filePath = None
        self.path = QDir.homePath()

        self.labelMessage = QLabel('')
        self.labelCoordinates = QLabel('')
        self.statusProgressBar = QProgressBar(self)
        self.statusBar.addPermanentWidget(self.labelMessage, 0)
        self.statusBar.addPermanentWidget(self.statusProgressBar, 1)
        self.statusBar.addPermanentWidget(self.labelCoordinates, 2)

        self.zoomWidget = ZoomWidget()
        self.canvas = Canvas(parent=self)
        self.scrollArea.setWidget(self.canvas)
        self.canvas.scrollRequest.connect(self.scrollRequest)
        self.canvas.newShape.connect(self.newShape)
        self.canvas.shapeMoved.connect(self.shapeMoved)
        self.canvas.selectionChanged.connect(self.shapeSelectionChanged)

        # self.canvas.zoomRequest.connect(self.zoomNavig.zoomRequest)
        self.canvas.zoomRequest.connect(self.zoomRequest)

        self.previous_shape = []

        self.videolen = 0
        self.scrollBars = {
            Qt.Vertical: self.scrollArea.verticalScrollBar(),
            Qt.Horizontal: self.scrollArea.horizontalScrollBar()
        }

        #set Icon for buttons
        self.playButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))
        self.nextButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.prevButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        # setup connection
        self.playButton.clicked.connect(self.playPause)
        self.changePixmapIndex.connect(self.setPosition)

        self.nextButton.clicked.connect(self.nextFrame)
        self.prevButton.clicked.connect(self.prevFrame)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.actionOpen_Video.triggered.connect(self.openVideo)
        self.actionSave_Annotation.triggered.connect(self.saveAnnotations)
        self.actionSave_Annotation_As.triggered.connect(self.saveAnnotationsAs)
        self.actionExit.triggered.connect(self.exitCall)

        # Set Tracking
        self.removeTracker.clicked.connect(self.removeTrackerClicked)
        self.addTracker.clicked.connect(self.addTrackerClicked)
        self.stopTracker.clicked.connect(self.stopTrackerClicked)
        self.continueTracker.clicked.connect(self.continueTrackerClicked)
        self.FPS = -1
        self.width = -1
        self.height = -1

        self._noSelectionSlot = False
        self.itemsToShapes = {}
        self.shapesToItems = {}

        self.logging("Application initialized")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.nextFrame)

    @pyqtSlot()
    def playPause(self):
        if self.timer.isActive():
            self.pause()
        else:
            self.play()

    def pause(self):
        logging.info('Pause Streaming')
        self.timer.stop()
        self.playButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))

    def play(self):
        logging.info('Play Streaming')
        self.timer.start(1000/self.FPS)
        self.playButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPause))

    def zoomRequest(self, delta):
        # get the current scrollbar positions
        # calculate the percentages ~ coordinates
        h_bar = self.scrollBars[Qt.Horizontal]
        v_bar = self.scrollBars[Qt.Vertical]

        # get the current maximum, to know the difference after zooming
        h_bar_max = h_bar.maximum()
        v_bar_max = v_bar.maximum()

        # get the cursor position and canvas size
        # calculate the desired movement from 0 to 1
        # where 0 = move left
        #       1 = move right
        # up and down analogous
        cursor = QCursor()
        pos = cursor.pos()
        relative_pos = QWidget.mapFromGlobal(self, pos)

        cursor_x = relative_pos.x()
        cursor_y = relative_pos.y()

        w = self.scrollArea.width()
        h = self.scrollArea.height()

        # the scaling from 0 to 1 has some padding
        # you don't have to hit the very leftmost pixel for a maximum-left movement
        margin = 0.1
        move_x = (cursor_x - margin * w) / (w - 2 * margin * w)
        move_y = (cursor_y - margin * h) / (h - 2 * margin * h)

        # clamp the values from 0 to 1
        move_x = min(max(move_x, 0), 1)
        move_y = min(max(move_y, 0), 1)

        # zoom in
        units = delta / (8 * 15)
        scale = 10
        self.addZoom(scale * units)

        # get the difference in scrollbar values
        # this is how far we can move
        d_h_bar_max = h_bar.maximum() - h_bar_max
        d_v_bar_max = v_bar.maximum() - v_bar_max

        # get the new scrollbar values
        new_h_bar_value = h_bar.value() + move_x * d_h_bar_max
        new_v_bar_value = v_bar.value() + move_y * d_v_bar_max

        h_bar.setValue(new_h_bar_value)
        v_bar.setValue(new_v_bar_value)


    def addZoom(self, increment=10):
        self.setZoom(self.zoomWidget.value() + increment)

    def setZoom(self, value):
        # self.actions.fitWidth.setChecked(False)
        # self.actions.fitWindow.setChecked(False)
        # self.zoomMode = self.MANUAL_ZOOM
        self.zoomWidget.setValue(value)

    def setPosition(self, index):
        if index < 0:
             index = 0

        if index >= self.videolen:
            self.pause()
            index = self.videolen-1

        self.previous_shape = self.canvas.shapes

        self.frame_index = index

        self.positionSlider.setValue(index)
        self.positionSlider.setToolTip(f"Frame {index}/{self.videolen}")
        self.timeLabel.setText(f"Frame {index}/{self.videolen}")

        self.rgbImage = self.videoFrames[index]

        h, w, ch = self.rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(
            self.rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        # .scaled(640, 480, Qt.KeepAspectRatio)
        self.QImage = convertToQtFormat

        self.canvas.loadPixmap(QPixmap.fromImage(self.QImage))

        if self.isTracking():
            self.processFrame(self.rgbImage)

        self.logging(f"Position set at time: {index/self.FPS:.3f} s")

    def nextFrame(self):
        self.changePixmapIndex.emit(self.frame_index+1)

    def prevFrame(self):
        self.changePixmapIndex.emit(self.frame_index-1)

    def handleError(self):
        self.centralwidget.setEnabled(False)
        self.logging("Error: " + self.mediaPlayer.errorString())

    def logging(self, message):
        logging.info(message)
        self.labelMessage.setText(message)
        # self.statusBar.showMessage(message)

    def openVideo(self, filename=False):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, "Open Video",
                                                      self.path)
        self.path = osp.dirname(str(filename))
        if filename != '':
            self.filePath = filename
            self.videoFrames = []

            # read FPS
            cap = cv2.VideoCapture(filename)
            FPS_real = cap.get(cv2.CAP_PROP_FPS)
            FPS_desired = 15
            self.FPS = FPS_desired if FPS_real > FPS_desired else FPS_real
            self.logging(
                f"FPS real:{FPS_real} / FPS desired: {FPS_desired} / FPS frames {self.FPS}")
            # read number frames
            videogen = skvideo.io.FFmpegReader(self.filePath)
            (numFiles, width, height, _) = videogen.getShape()
            videogen = skvideo.io.vreader(self.filePath)

            self.width = int(1920/2)
            self.height = int(1440/2)

            self.statusProgressBar.setMaximum(numFiles)
            self.statusProgressBar.setTextVisible(True);
            self.statusProgressBar.setFormat("Loading Video...");

            # read video fraems in the background
            args = (self, videogen, FPS_real,
                    FPS_desired, self.width, self.height)
            self.p = ProcessRunnable(target=runReadVideo, args=args)
            self.p.start()

            self.centralwidget.setEnabled(True)

    @pyqtSlot(QImage)
    def appendFrame(self, frame):
        ptr = frame.bits()
        ptr.setsize(frame.byteCount())
        cvframe = np.array(ptr).reshape(frame.height(), frame.width(), 3)

        self.videoFrames.append(cvframe)
        self.videolen = len(self.videoFrames)

        self.positionSlider.setMaximum(self.videolen-1)
        self.positionSlider.setMinimum(0)

        if self.videolen == 1:
            self.changePixmapIndex.emit(0)
            
        self.timeLabel.setText(f"Frame {self.frame_index}/{self.videolen}")
        self.statusProgressBar.setValue(self.videolen-1)


    def saveAnnotationsAs(self):
        filename = QFileDialog.getSaveFileName(self, "Save file", self.path, ".txt")[0]
        self.saveAnnotations(filename)

    def saveAnnotations(self, filename=None):
        print(filename)
        if filename is None or not filename:
            filename = os.path.splitext(self.filePath)[0]+".txt"

        print(filename)
        if filename == '':
            self.logging("Please select a path to save the annotations")
            return
        file_object = open(filename, "w") # as file_object:

        for i in range(self.listTracker.count()):
            this_item = self.listTracker.item(i)
            this_tracker = self.listTracker.itemWidget(this_item)
            # this_tracker.boxes
            for pos, box, _ in this_tracker:
                lineBB = f"{pos/self.FPS:10.3f}, {box[0]/self.width:.3f}, {box[1]/self.height:.3f}, {box[2]/self.width:.3f}, {box[3]/self.height:.3f} \n"
                print(lineBB)
                file_object.write(lineBB)
        file_object.close()
        print("done saving")

    def exitCall(self):
        self.logging("Exiting the application")
        sys.exit(app.exec_())

    def shapeMoved(self):
        self.previous_shape = self.canvas.shapes
        for shape in self.canvas.shapes:
            item = self.shapesToItems[shape]
            tracker = self.listTracker.itemWidget(item)
            tracker.resetTracker(new_state=tuple(shape2box(shape)))

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

    def isTracking(self, pos=None):
        # print("isTracking?")
        if pos is None:
            pos = self.frame_index
            # pos = self. self.mediaPlayer.position()

        for i in range(self.listTracker.count()):
            this_item = self.listTracker.item(i)
            this_tracker = self.listTracker.itemWidget(this_item)
            if this_tracker.isTracking(pos):
                return True
        return False

    def processFrame(self, videoFrame):
        currentPos = self.frame_index


        new_shapes = []

        # List shape already drawn previously
        for i in range(self.listTracker.count()):
            this_item = self.listTracker.item(i)
            this_tracker = self.listTracker.itemWidget(this_item)
            if self.frame_index in this_tracker.times:

                new_box = this_tracker.boxes[this_tracker.times.index(
                    self.frame_index)]

                new_shape = box2shape(new_box, label="Tracker")
                new_shapes.append(new_shape)

                self.itemsToShapes[this_item] = new_shape
                self.shapesToItems[new_shape] = this_item

        # List shape from previous canvas, for tracking
        for shape in self.previous_shape:
            # if shape not in self.shapesToItems:
            #     continue
            this_item = self.shapesToItems[shape]
            this_tracker = self.listTracker.itemWidget(this_item)
            if this_tracker.isTracking(currentPos):
                # self.surface
                if currentPos in this_tracker.times:
                    print("already tracked!")
                    continue

                success, new_box = this_tracker.runTracker(
                    self.rgbImage, currentPos)

                if not success: 
                    print("end tracked")
                    self.pause()
                    continue

                new_shape = box2shape(new_box, label="Tracker")
                new_shapes.append(new_shape)

                self.itemsToShapes[this_item] = new_shape
                self.shapesToItems[new_shape] = this_item

        self.canvas.loadShapes(new_shapes)
        # self.canvas.shapes = new_shapes
        # self.canvas.repaint()


    def stopTrackerClicked(self):

        current_item = self.listTracker.currentItem()
        current_tracker = self.listTracker.itemWidget(current_item)
        if current_tracker.isTracking(self.frame_index):
            current_tracker.stop_frame = self.frame_index
            current_tracker.updateItem()
        else:
            self.logging("Tracker already done")

        self.stopTracker.setEnabled(self.listTracker.count() > 0)

    def removeTrackerClicked(self):
        current_item = self.listTracker.currentItem()
        current_shape = self.itemsToShapes[current_item]
        if current_shape in self.canvas.shapes:
            self.canvas.shapes.remove(current_shape)

        self.canvas.repaint()
        self.listTracker.takeItem(self.listTracker.row(current_item))


    def addTrackerClicked(self):
        self.canvas.setEditing(False)
        self.appendShape = False

    def continueTrackerClicked(self):
        self.canvas.setEditing(False)
        self.appendShape = True

    def newShape(self):
        """Pop-up and give focus to the label editor.
        position MUST be in global coordinates.
        """
        self.canvas.setEditing(True)
        shape = self.canvas.setLastLabel("Tracker")

        current_box = shape2box(shape)
        if self.appendShape:
            # this_item = self.listTracker.item(i)

            current_item = self.listTracker.currentItem()
            current_tracker = self.listTracker.itemWidget(current_item)
            # current_tracker.

            current_tracker.times.append(self.frame_index)
            current_tracker.frames.append(self.rgbImage)
            current_tracker.boxes.append(current_box)
            current_tracker.stop_frame = -1
            current_tracker.updateItem()
            current_tracker.resetTracker(new_state=tuple(current_box))

            # this_item = self.shapesToItems[shape]
            self.itemsToShapes[current_item] = shape
            self.shapesToItems[shape] = current_item

            self.canvas.repaint()
            # self.listTracker.takeItem(self.listTracker.row(current_item))

        else:
            new_tracker = Tracker(start_frame=self.frame_index,
                                  stop_frame=-1,
                                  init_CVImage=self.rgbImage,
                                  init_box=current_box,
                                  selectTracker=str(self.selectTracker.currentText()))


            item = HashableQListWidgetItem(self.listTracker)
            item.setSizeHint(new_tracker.minimumSizeHint())

            self.listTracker.addItem(item)

            self.listTracker.setItemWidget(item, new_tracker)
            self.listTracker.setCurrentItem(item)

            self.itemsToShapes[item] = shape
            self.shapesToItems[shape] = item

        self.stopTracker.setEnabled(self.listTracker.count() > 0)


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
    def __init__(self, start_frame, stop_frame, init_box, init_CVImage, selectTracker="kcf", parent=None):
        super(Tracker, self).__init__(parent)
        self.selectTracker = selectTracker
        self.start_frame = start_frame
        self.stop_frame = stop_frame
        self.boxes = [init_box]
        self.frames = [init_CVImage]
        self.times = [self.start_frame]

        # get thumbnail of object
        h, w, ch = self.frames[-1].shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(
            self.frames[-1].data, w, h, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(convertToQtFormat)
        pixmap = pixmap.copy(
            QRect(init_box[0], init_box[1], init_box[2], init_box[3]))
        pixmap = pixmap.scaled(20, 20, QtCore.Qt.KeepAspectRatio)
        self.iconQLabel = QLabel()
        self.iconQLabel.setPixmap(pixmap)

        self.nameQLabel = QLabel()
        self.nameQLabel.setText(self.getName())

        self.row = QHBoxLayout()
        self.row.addWidget(self.iconQLabel)
        self.row.addWidget(self.nameQLabel)
        self.setLayout(self.row)


        self.tracker = OPENCV_OBJECT_TRACKERS[self.selectTracker]()

        self.tracker.init(self.frames[0], tuple(init_box))

    def QImage2CVImage(self, myQimg):
        ptr = myQimg.bits()
        ptr.setsize(myQimg.byteCount())
        return np.array(ptr).reshape(myQimg.height(), myQimg.width(), 4)

    def resetTracker(self, new_state):
        self.tracker.clear()
        self.tracker = OPENCV_OBJECT_TRACKERS[self.selectTracker]()
        self.tracker.init(self.frames[-1], new_state)

    def runTracker(self, qimage, pos):

        (success, box) = self.tracker.update(qimage)

        if not success:
            self.stop_frame = self.times[-1]  
            self.updateItem()
            return success, box

        self.times.append(pos)
        self.frames.append(qimage)
        self.boxes.append(box)
        return success, self.boxes[-1]

    def __getitem__(self, i):
        return self.times[i], self.boxes[i], self.frames[i]

    def isTracking(self, pos):
        return not self.afterTracking(pos) and not self.beforeTracking(pos)

    def afterTracking(self, pos):
        return pos >= self.stop_frame and self.stop_frame > 0

    def beforeTracking(self, pos):
        return pos < self.start_frame

    def updateItem(self):
        self.nameQLabel.setText(self.getName())

    def box2rect(self, box):
        return QRect(box[0], box[1], box[2], box[3])

    def getName(self):
        return f"Tracker {self.selectTracker} from frame {self.start_frame} to {self.stop_frame}"



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
