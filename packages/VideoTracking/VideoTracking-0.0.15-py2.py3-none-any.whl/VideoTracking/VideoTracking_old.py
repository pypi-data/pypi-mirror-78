#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import logging
from datetime import datetime
import getpass

from PyQt5.QtWidgets import QApplication

from src.TrackingWindow import TrackingWindow 

__version__= "0.0.1"

def main():
    '''construct main app and run it'''

    # Argument Parser
    parser = argparse.ArgumentParser(
        description="Image Labeler based on Active Learning")
    # parser.add_argument("--host",
    #             default="127.0.0.1",
    #             type=str,
    #             help="host to connect to API")

    # parser.add_argument("--port",
    #                     default=8000,
    #                     type=int,
    #                     help="port to connect to API")

    # parser.add_argument("--project",
    #                     default=None,
    #                     type=str,
    #                     help="open a project")

    parser.add_argument("--logdir",
                        default="log",
                        type=str,
                        help="diretory for logging")

    parser.add_argument("--loglevel",
                        default="INFO",
                        type=str,
                        help="diretory for logging")

    args = parser.parse_args()
        
    # define logging level (DEBUG/INFO/WARNING/ERROR)
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel)

    # set up logging configuration
    log_file = os.path.join(args.logdir, datetime.now().strftime('%Y-%m-%d %H-%M-%S.log'))
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        level=numeric_level, # INFO
        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        handlers=[
            # file handler
            logging.FileHandler(log_file),
            # stream handler
            logging.StreamHandler()
        ])
    logging.info(f"Start logging on {log_file}")
    logging.info(f"Starting Videotracking version {__version__}")



    # if getpass.getuser() not in "giancos":
    #     # send report on SLACK for users different from the authors
    #     sys.excepthook = excepthook

    # create QtApplication
    app = QApplication(sys.argv)
    # app.setApplicationName("Seeds Labeler")
    # app.setWindowIcon(newIcon("shape_t"))

    # Create GUI
    win = TrackingWindow()
    # # Create API    
    # api = InferenceApi(win.serverHost.text(),
    #                    win.serverPort.value(), win.serverProject.currentText())


    # win.widget = QVideoWidget(win.centralwidget)
    # win.widget.setObjectName("widget")

    # win.centralwidget = QVideoWidget()
    # player = QMediaPlayer()
    # player.setMedia(QMediaContent(QUrl.fromLocalFile(video_file)))
    # player.setVideoOutput(win.widget)
    # player.play()
    
    # # Connect API to GUI
    # win.serverHost.textChanged.connect(api.setHost)
    # win.serverPort.valueChanged.connect(api.setPort)
    # win.serverProject.currentTextChanged.connect(api.setProject)
    # # GUI detection button connected to API Object Detection
    # # (parameter is OpenCV Image)
    # win.detect.triggered.connect(lambda: api.detectObjects(win.currentImage.path))

    # # API Object Found connected to Window add Shape to current Image
    # api.objectFound.connect(win.addShape)
    # api.objectsFound.connect(win.addShapes)
    # api.errorWithInference.connect(win.errorMessage)

    # Show window and run QtApplication
    win.showMaximized()
    # win.show()

    # open project if asked to with arguments
    # if args.project is not None:
        # win.openProject(args.project)

    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
