#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import logging


# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow, QProgressDialog, QMessageBox, QFileDialog, QPushButton, QMenu
from PyQt5.QtCore import QSettings, QThread, Qt, pyqtSignal, pyqtSlot, QTimer, QUrl, QPointF
from PyQt5.QtGui import QImage, QPixmap, QKeySequence

from functools import partial
# from PyQt5.QtMultimediaWidgets import QVideoWidget
# from PyQt5.QtCore import QUrl
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

# env_path = os.path.join(os.path.dirname(__file__), 'pysot')
# print(sys.path)
# if env_path not in sys.path:
#     sys.path.append(env_path)
#     print(sys.path)

# from pysot.core.config import cfg
# from pysot.models.model_builder import ModelBuilder
# from pysot.tracker.tracker_builder import build_tracker

# from motpy import Detection, MultiObjectTracker
import cv2
OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
}


from src.ui_mainwindow import Ui_MainWindow  #as LabelerWindow
from src.utils import *
from libs.canvas import Canvas
from libs.labelDialog import LabelDialog
from libs.lib import generateColorByText, addActions, newAction
from libs.labelFile import LabelFile
from libs.hashableQListWidgetItem import HashableQListWidgetItem
from libs.shape import Shape, DEFAULT_LINE_COLOR, DEFAULT_FILL_COLOR

# , generateColorByText
# from src.libs.lib import struct, newAction, newIcon, addActions, fmtShortcut


import skvideo.io
import skvideo.datasets

class TrackingWindow(QMainWindow, Ui_MainWindow):

    changePixmapIndex = pyqtSignal(int)

    def __init__(self):
        super(TrackingWindow, self).__init__()
        self.setupUi(self)

        tracker = cv2.TrackerKCF_create()

        self.labelCoordinates = QLabel('')
        self.statusBar().addPermanentWidget(self.labelCoordinates)

        self.lastOpenDir = None
        self.frame_index = 0
        self.tracking = False
        self.shapes = None
        self.canvas = Canvas(parent=self)
        self.scroll.setWidget(self.canvas)

        self.dirty = False
        self._noSelectionSlot = False
        self.itemsToShapes = {}
        self.shapesToItems = {}
        self.prevLabelText = ''

        # self.videofile =  "/home/giancos/Downloads/GH010003.MP4" # skvideo.datasets.bigbuckbunny()
        self.mImgList = []
        self.dirname = None

        self.labelHist = []
        self.lastLabel = None
        self.labelDialog = LabelDialog(parent=self, listItem=self.labelHist)

        self.loadSettings()
        # self.frame_index=0


        # self.X = 0
        # self.Y = 0
        self.changePixmapIndex.connect(self.setImageIndex)
        self.pushButton_Next.clicked.connect(self.nextFrame)
        self.pushButton_Prev.clicked.connect(self.prevFrame)
        self.openVideoSignal.triggered.connect(self.openVideoAction)
        self.deleteAction.triggered.connect(self.deleteSelectedShape)
        self.deleteAction.setShortcuts(QKeySequence("Backspace, Del"))
        self.saveAs.triggered.connect(self.saveAnnotations)


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.nextFrame)

        self.pushButton_PlayPause.clicked.connect(self.playPause)
        self.pushButton_Rewind.clicked.connect(self.rewind)
        self.spinBox_FPS.valueChanged.connect(self.changeFPS)

        self.horizontalSlider_time.valueChanged.connect(self.setImageIndex)
        # self.changePixmapIndex.emit(0)
        # self.label_videoframe.mouseMoveEvent = self.getPos

        self.scrollBars = {
            Qt.Vertical: self.scroll.verticalScrollBar(),
            Qt.Horizontal: self.scroll.horizontalScrollBar()
        }

        
         ###CANVAS
        self.canvas.scrollRequest.connect(self.scrollRequest)
        self.canvas.newShape.connect(self.newShape)
        # self.canvas.newShapes.connect(self.newShapes)
        self.canvas.shapeMoved.connect(self.setDirty)
        self.canvas.selectionChanged.connect(self.shapeSelectionChanged)
        # self.canvas.drawingPolygon.connect(self.toggleDrawingSensitive)        
        # self.canvas.zoomRequest.connect(self.zoomNavig.zoomRequest)

        # submenu for hide/show
        self.hideShowMenu = QMenu("Hide/Show")
        # addActions(self.hideShowMenu, (self.hideCurrentClass,
        #                                self.showCurrentClass, self.hideAll, self.showAll))

        # submenu for hide/show
        self.labelMenu = QMenu()
        addActions(self.labelMenu, (self.edit,
                                    self.deleteAction, self.hideShowMenu))
        addActions(self.canvas.menus[0], (self.create,
                                          self.edit, self.deleteAction, self.hideShowMenu))

        # right click drag
        action = partial(newAction, self)
        addActions(self.canvas.menus[1], (
            action('&Copy here', self.copyShape),
            action('&Move here', self.moveShape)))

        #TRACK

        self.actionAdd_Track.triggered.connect(self.addTrack)
        self.filePath = skvideo.datasets.bigbuckbunny()
        self.openVideo(self.filePath)
        
        self.trackers = cv2.MultiTracker_create()

    def remLabel(self, shape):
        if shape is None:
            # print('rm empty label')
            return
        item = self.shapesToItems[shape]
        self.labelList.takeItem(self.labelList.row(item))
        self.shapes.remove(shape)
        del self.shapesToItems[shape]
        del self.itemsToShapes[item]
        # self.updateCount()

    def noShapes(self):
        return not self.itemsToShapes

    def deleteSelectedShape(self):
        self.remLabel(self.canvas.deleteSelected())
        self.setDirty()
        # if self.noShapes():
            # for action in self.actions.onShapesPresent:
                # action.setEnabled(False)

    def copyShape(self):
        self.canvas.endMove(copy=True)
        self.addLabel(self.canvas.selectedShape)
        self.setFileChanged()

    def moveShape(self):
        self.canvas.endMove(copy=False)
        self.setFileChanged()

    def resetState(self):
        self.itemsToShapes.clear()
        self.shapesToItems.clear()
        self.labelList.clear()
        self.filePath = None
        self.imageData = None
        self.labelFile = None
        self.canvas.resetState()
        self.labelCoordinates.clear()
        self.comboBox.cb.clear()

    def addTrack(self):
        # self.toggleDrawMode(False)
        self.canvas.setEditing(False)
        self.actionAdd_Track.setEnabled(False)

        # self.createMode.setEnabled(edit)
        # self.editMode.setEnabled(not edit)

    # def toggleDrawMode(self, edit=True):
        # self.canvas.setEditing(edit)
        # self.createMode.setEnabled(edit)
        # self.editMode.setEnabled(not edit)

    def toggleDrawingSensitive(self, drawing=True):
        """In the middle of drawing, toggling between modes should be disabled."""
        # self.actions.editMode.setEnabled(not drawing)
        if not drawing:
            # Cancel creation.
            print('Cancel creation.')
            self.canvas.setEditing(True)
            self.canvas.restoreCursor()
            self.actionAdd_Track.setEnabled(True)

    # React to canvas signals.
    def shapeSelectionChanged(self, selected=False):
        if self._noSelectionSlot:
            self._noSelectionSlot = False
        else:
            shape = self.canvas.selectedShape
            if shape:
                self.shapesToItems[shape].setSelected(True)
            else:
                self.labelList.clearSelection()
        self.deleteAction.setEnabled(selected)
        # self.actions.copy.setEnabled(selected)
        # self.actions.edit.setEnabled(selected)
        # self.actions.shapeLineColor.setEnabled(selected)
        # self.actions.shapeFillColor.setEnabled(selected)

    def setDirty(self):
        self.dirty = True
        # self.actions.save.setEnabled(True)

    # Callback functions:
    def newShape(self):
        """Pop-up and give focus to the label editor.
        position MUST be in global coordinates.
        """
        logging.info("newShapes")
        # if not self.useDefaultLabelCheckbox.isChecked() or not self.defaultLabelTextLine.text():
        if len(self.labelHist) > 0:
            self.labelDialog = LabelDialog(
                parent=self, listItem=self.labelHist)

        # Sync single class mode from PR#106
        if False and self.lastLabel:
            text = self.lastLabel
        else:
            text = self.labelDialog.popUp(text=self.prevLabelText)
            self.lastLabel = text
        # else:
        #     text = self.defaultLabelTextLine.text()
        # text = "trackee"

        # # Add Chris
        if text is not None:
            self.prevLabelText = text
            generate_color = generateColorByText(text)
            shape = self.canvas.setLastLabel(text, generate_color, generate_color)
            self.addLabel(shape)
            
            if True: #self.beginner():  # Switch to edit mode.
                self.canvas.setEditing(True)
                self.actionAdd_Track.setEnabled(True)
            else:
                self.actions.editMode.setEnabled(True)
            self.setDirty()

            if text not in self.labelHist:
                self.labelHist.append(text)
        else:
            self.canvas.resetAllLines()
        self.canvas.setEditing(True)
        # self.create.setEnabled(True)
        


    def addLabel(self, shape, addtracker=True):
        # shape.paintLabel = self.displayLabelOption.isChecked()
        item = HashableQListWidgetItem(f"Frame {self.frame_index} - {shape.label}")
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Checked)
        item.setBackground(generateColorByText(shape.label))
        self.itemsToShapes[item] = shape
        self.shapesToItems[shape] = item
        self.labelList.addItem(item)


        self.shapes.append(shape)


        if addtracker:
            tracker = OPENCV_OBJECT_TRACKERS["csrt"]()
            box = shape2box(shape)
            self.trackers.add(tracker, self.rgbImage, box)
            (success, boxes) = self.trackers.update(self.rgbImage)



    def scrollRequest(self, delta, orientation):
        units = - delta / (8 * 15)
        bar = self.scrollBars[orientation]
        bar.setValue(bar.value() + bar.singleStep() * units)

    def getPos(self, event):
        x = event.x()
        y = event.y()
        # print("width", self.label_videoframe.width)
        print(x, y)
        self.X = x
        self.Y = y 
        # self.label_videoframe.setPixmap(QPixmap.fromImage(self.QImage))

        self.printImage()

    @pyqtSlot()
    def playPause(self):
        if self.timer.isActive():
            self.pause()
        else:
            self.play()

    def pause(self):
        logging.info('Pause Streaming')
        self.timer.stop()
        self.pushButton_PlayPause.setText("Play")

    def play(self):
        logging.info('Play Streaming')
        self.timer.start(1000/self.spinBox_FPS.value())
        self.pushButton_PlayPause.setText("Pause")

    @pyqtSlot()
    def openVideoAction(self):
        filename = QFileDialog.getOpenFileName(self, "Select the video to process", self.lastOpenDir)[0]
        if filename == "":
            return
        self.lastOpenDir = os.path.dirname(os.path.abspath(filename))
        self.openVideo(filename)


    def openVideo(self, path):
        self.filePath = path
        import time
        start_time = time.time()
        videogen = skvideo.io.FFmpegReader(path)
        (numFiles, _, _, _) = videogen.getShape()
        # QProgressDialog progress("Copying files...", "Abort Copy", 0, numFiles, this);
        progress = QProgressDialog("Reading frames...", "Abort Reading", 0, numFiles, self)
        progress.setWindowModality(Qt.WindowModal)

        self.videoFrames = []
        self.videoLabels = []
        for i, frame in enumerate(videogen):

            progress.setValue(i)

            if progress.wasCanceled():
                break

            self.videoFrames.append(frame)
            self.videoLabels.append([])
        
        progress.setValue(numFiles)

        self.videolen = len(self.videoFrames)

        elapsed_time = time.time() - start_time
        logging.info(f'Opening Video: {self.videolen} frames read in {elapsed_time:.3f}s')
        
        self.horizontalSlider_time.setMaximum(self.videolen-1)
        self.horizontalSlider_time.setMinimum(0)
        self.changePixmapIndex.emit(0)


    def saveAnnotations(self):
        filename = QFileDialog.getSaveFileName(
            self, 'Save Annotations', '', "Text Files (*.txt);;All Files (*)")[0]
        logging.info(f"Saving Bounding boxes in {filename}")

        with open(filename, 'w') as f1:

            for i, shapes in enumerate(self.videoLabels):
                for shape in shapes:
                    print(i, shape.label, shape2box(shape))
                    box = shape2box(shape)
                    content = f"{i}, {shape.label}, {box[0]}, {box[1]}, {box[2]}, {box[3]}"
                    f1.write(content + os.linesep)



    def loadLabels(self, shapes):
        s = []
        for label, points, line_color, fill_color, difficult in shapes:
            shape = Shape(label=label)
            for x, y in points:

                # Ensure the labels are within the bounds of the image. If not, fix them.
                x, y, snapped = self.canvas.snapPointToCanvas(x, y)
                if snapped:
                    self.setDirty()

                shape.addPoint(QPointF(x, y))
            shape.difficult = difficult
            shape.close()
            s.append(shape)

            if line_color:
                shape.line_color = QColor(*line_color)
            else:
                shape.line_color = generateColorByText(label)

            if fill_color:
                shape.fill_color = QColor(*fill_color)
            else:
                shape.fill_color = generateColorByText(label)

            self.addLabel(shape)

        self.canvas.loadShapes(s)


    @pyqtSlot()
    def rewind(self):
        self.timer.stop()
        self.changePixmapIndex.emit(0)

    @pyqtSlot()
    def changeFPS(self):
        if self.timer.isActive():
            self.pause()
            self.play()

    @pyqtSlot()
    def nextFrame(self):
        if self.checkBox_Tracking.isChecked():
            self.tracking = True
        
        self.changePixmapIndex.emit(self.frame_index+1)
        

    @pyqtSlot()
    def prevFrame(self):
        self.changePixmapIndex.emit(self.frame_index-1)

    @pyqtSlot(int)
    def setImageIndex(self, index):

        logging.info(f'Reading frame {index}')


        
        if index < 0:
             index = 0

        if index >= self.videolen:
            self.pause()
            self.tracking = False
            index = self.videolen-1

        self.frame_index = index

        self.horizontalSlider_time.setValue(index)
        self.horizontalSlider_time.setToolTip(f"Frame {index}/{self.videolen}")
        self.label_Frame.setText(f"Frame {index}/{self.videolen}")

        # self.cap.set(2,index);
        # self.rgbImage_vd = self.videoFrames[self.frame_index,:,:,:] # = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.rgbImage = self.videoFrames[index]
        # self.shapes = 
        self.prev_shapes = self.shapes
        self.shapes = self.videoLabels[index]



        if self.tracking:

            # REASSIGN TRACKER EVERY FRAME
            # trackers = cv2.MultiTracker_create()
            # tracker = OPENCV_OBJECT_TRACKERS["csrt"]()

            # for shape in self.prev_shapes:
            #     box = shape2box(shape)
            #     trackers.add(tracker, self.rgbImage, box)
            #     print("add box")
            
            # (success, boxes) = trackers.update(self.rgbImage)
            # print("update tracker", success, boxes)
            # (success, boxes) = trackers.update(self.rgbImage)
            # print("update tracker", success, boxes)


            # for shape, tracked_box in zip(self.prev_shapes, boxes):
            #     # print(shape)
            #     # print(tracked_box)
            #     new_shape = box2shape(tracked_box, shape.label)
            #     overlapping = False
            #     for existing_shape in self.shapes:
            #         if IOU(new_shape, existing_shape) > 0.3:
            #             overlapping = True
            #             break
            #     if not overlapping:
            #         self.addLabel(new_shape, addtracker=False)


            # KEEP GLOBAL TRACKING
            (success, boxes) = self.trackers.update(self.rgbImage)
            print(success, boxes)
            for shape, tracked_box in zip(self.prev_shapes, boxes):
                # print(shape)
                # print(tracked_box)
                new_shape = box2shape(tracked_box, shape.label)
                overlapping = False
                for prev_shape in self.shapes:
                    if IOU(new_shape, prev_shape) > 0.3:
                        overlapping = True
                        break
                if not overlapping:
                    self.addLabel(new_shape, addtracker=False)

            # COPY BOXES AS IS
            # for box in self.prev_shapes:
            #     good = True
            #     for prev_box in self.shapes:
            #         if IOU(box, prev_box)>0.3:
            #             good = False
            #             break

            #     if good:
            #         self.addLabel(box.copy())
                
        

        self.printImage()

        self.tracking = False

    def printImage(self):
        h, w, ch = self.rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(self.rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        self.QImage = convertToQtFormat #.scaled(640, 480, Qt.KeepAspectRatio)
        # self.label_videoframe.setPixmap(QPixmap.fromImage(self.QImage))
        
        self.canvas.loadPixmap(QPixmap.fromImage(self.QImage))
        # if self.labelList
        # print(self.shapes)
        self.canvas.loadShapes(self.shapes)
        # self.shapes


    def closeEvent(self, event):
        self.saveSettings()


    def loadSettings(self):
        # read server parameters
        logging.info('Reading Settings')
        settings = QSettings('KAUST_IVUL', 'VideoTracking')
        # set server parameters
        # self.videofile = skvideo.datasets.bigbuckbunny()
        self.spinBox_FPS.setValue(settings.value('video_FPS', 25, int))
        self.lastOpenDir = settings.value('video_Directory', "", str)
        # self.videofile = settings.value('video_File', skvideo.datasets.bigbuckbunny(), str)

        # self.serverHost.setText(settings.value('serverHost', "localhost", str))
        # self.serverPort.setValue(settings.value('serverPort', 8000, int))
        # self.serverProject.setCurrentText(settings.value('serverProject', "Striga_Strat1", str))


    def saveSettings(self):        
        # save server parameters
        logging.info('Saving Settings')
        settings = QSettings('KAUST_IVUL', 'VideoTracking')
        # read server parameters
        settings.setValue('video_FPS', self.spinBox_FPS.value())
        settings.setValue('video_Directory', self.lastOpenDir)
        # settings.setValue('video_File', self.videofile)

        # settings.setValue('serverHost', self.serverHost.text())
        # settings.setValue('serverPort', self.serverPort.value())
        # settings.setValue('serverProject', self.serverProject.currentText())
