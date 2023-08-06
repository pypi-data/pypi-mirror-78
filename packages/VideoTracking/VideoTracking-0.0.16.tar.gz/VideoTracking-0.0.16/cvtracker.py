import cv2

import skvideo.io
import skvideo.datasets

OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
}
# initialize OpenCV's special multi-object tracker
trackers = cv2.MultiTracker_create()
tracker = OPENCV_OBJECT_TRACKERS["mosse"]()



videoFrames = []
videogen = skvideo.io.FFmpegReader(skvideo.datasets.bigbuckbunny())
for frame in videogen:
    videoFrames.append(frame)


frame = videoFrames[0]
box = (301, 256, 356-301, 353-256)
trackers.add(tracker, frame, box)
(success, boxes) = trackers.update(frame)
print("init", box)


frame = videoFrames[1]
(success, boxes) = trackers.update(frame)
print(success, boxes)

# frame = videoFrames[2]
(success, boxes) = trackers.update(frame)
print(success, boxes)

# frame = videoFrames[3]
(success, boxes) = trackers.update(frame)
print(success, boxes)


