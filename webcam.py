import numpy as np
import os
import cv2
import time
import argparse

ap = argparse.ArgumentParser(description="")

ap.add_argument("-i", "--input", type=str, default="0", help="path to input video file")

args = vars(ap.parse_args())

# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

video_filename = 'new_video.avi'
image_filename = ''

frames_per_second = 12
res = '720p'

# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']

if args["input"] != "0":
	cap = cv2.VideoCapture(args["input"])
else:
	cap = cv2.VideoCapture(0)

out = cv2.VideoWriter(video_filename, get_video_type(video_filename), frames_per_second, get_dims(cap, res))

# cap.set(cv2.cv.CV_CAP_PROP_FPS, 6)

counter = 0

while True:
    
    ret, frame = cap.read()
    # Handles the mirroring of the current frame
    frame = cv2.flip(frame, 1)

    cv2.imshow('frame', frame)

    
    out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()