# VideoTracking
User Interface for Single Object Tracking on Videos

## Environment

```bash
conda create -y -n VideoTracking python=3.7
conda activate VideoTracking
pip install lxml pyqt5 numpy pandas requests opencv-python==4.1.1.26 #3.4.11.41
pip install scikit-video decord
pip install torch torchvision
# conda install -c conda-forge gst-python
# opencv-python==4.1.1.26
# opencv-contrib-python==3.4.5.20
# pip install lxml pyqt5 numpy pandas requests openpyxl opencv-python==4.1.1.26 matplotlib pynput
```


## Run 

pyuic5 src/mainwindow.ui -o src/ui_mainwindow.py; python VideoTracking.py