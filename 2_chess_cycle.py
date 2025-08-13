# Copyright (C) 2019 Eugene Pomazov, <stereopi.com>, virt2real team
#
# This file is part of StereoPi tutorial scripts.
#
# StereoPi tutorial is free software: you can redistribute it 
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the 
# License, or (at your option) any later version.
#
# StereoPi tutorial is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with StereoPi tutorial.  
# If not, see <http://www.gnu.org/licenses/>.
#
# Most of this code is updated version of 3dberry.org project by virt2real
# 
# Thanks to Adrian and http://pyimagesearch.com, as there are lot of
# code in this tutorial was taken from his lessons.
# 

import sys
import subprocess

try:
    import numpy as np
    np_version = np.__version__
    if np_version.startswith('2'):
        print("WARNING: NumPy 2.x detected. OpenCV requires NumPy 1.x")
        print("Attempting to downgrade NumPy...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy<2"])
        print("Please restart the script after NumPy downgrade")
        sys.exit(1)
except ImportError:
    print("Installing compatible NumPy version...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy<2"])
    print("Please restart the script after NumPy installation")
    sys.exit(1)

import time
from datetime import datetime
from picamera2 import Picamera2
import libcamera
import cv2
import numpy as np

# Photo session settings
total_photos = 30           
countdown = 3          # Changed from 5 to 2 seconds
font=cv2.FONT_HERSHEY_SIMPLEX 
 
# Camera settings
cam_width = 1280              # Total width for both cameras
cam_height = 480              
scale_ratio = 0.5

# Each camera gets half the total width
single_cam_width = cam_width // 2
cam_width = int((cam_width+31)/32)*32
cam_height = int((cam_height+15)/16)*16
print("Used camera resolution: "+str(cam_width)+" x "+str(cam_height))

# Buffer for captured image settings
img_width = int(cam_width * scale_ratio)
img_height = int(cam_height * scale_ratio)
print("Scaled image resolution: "+str(img_width)+" x "+str(img_height))

# Initialize both cameras
picam2_left = Picamera2(0)
picam2_right = Picamera2(1)

# Configure cameras
config_left = picam2_left.create_still_configuration(
    main={"size": (single_cam_width, cam_height)},
    transform=libcamera.Transform(hflip=True, vflip=False)  # Added vflip for 180-degree rotation
)
config_right = picam2_right.create_still_configuration(
    main={"size": (single_cam_width, cam_height)},
    transform=libcamera.Transform(hflip=True, vflip=False)  # Added vflip for 180-degree rotation
)

picam2_left.configure(config_left)
picam2_right.configure(config_right)
picam2_left.start()
picam2_right.start()
time.sleep(2)  # Warm-up time

# Start taking photos
counter = 0
t2 = datetime.now()
print("Starting photo sequence")

while True:
    # Capture from both cameras
    left_frame = picam2_left.capture_array("main")
    right_frame = picam2_right.capture_array("main")
    
    # Convert BGR to RGB
    left_frame = cv2.cvtColor(left_frame, cv2.COLOR_BGR2RGB)
    right_frame = cv2.cvtColor(right_frame, cv2.COLOR_BGR2RGB)
    
    # Combine frames side by side
    frame = np.hstack((left_frame, right_frame))
    frame = cv2.resize(frame, (img_width, img_height))
    
    t1 = datetime.now()
    cntdwn_timer = countdown - int((t1-t2).total_seconds())
    
    if cntdwn_timer == -1:
        counter += 1
        filename = f'./scenes/scene_{img_width}x{img_height}_{counter}.png'
        cv2.imwrite(filename, frame)
        print(f' [{counter} of {total_photos}] {filename}')
        t2 = datetime.now()
        # Removed sleep(1) to make captures faster
        cntdwn_timer = 0
        continue
        
    cv2.putText(frame, str(cntdwn_timer), (50,50), font, 2.0, (0,0,255), 4, cv2.LINE_AA)
    cv2.imshow("pair", frame)
    key = cv2.waitKey(1) & 0xFF
    
    if (key == ord("q")) | (counter == total_photos):
        break

print("Photo sequence finished")
picam2_left.stop()
picam2_right.stop()

