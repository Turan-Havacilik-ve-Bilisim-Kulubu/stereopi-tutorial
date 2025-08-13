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


from picamera2 import Picamera2
import time
import cv2
import numpy as np
import os
from datetime import datetime
from stereo_config import init_stereo_cameras

# File for captured image
filename = './scenes/photo.png'

# Camera settings
cam_width = 1280
cam_height = 480

# Final image capture settings
scale_ratio = 0.5

single_cam_width = cam_width // 2
cam_width = int((cam_width+31)/32)*32
cam_height = int((cam_height+15)/16)*16
print("Used camera resolution: "+str(cam_width)+" x "+str(cam_height))

# Calculate scaled dimensions
img_width = int(cam_width * scale_ratio)
img_height = int(cam_height * scale_ratio)
print("Scaled image resolution: "+str(img_width)+" x "+str(img_height))

# Initialize the stereo cameras
left_cam, right_cam = init_stereo_cameras()

# Start both cameras
left_cam.start()
right_cam.start()

t2 = datetime.now()
counter = 0
avgtime = 0

try:
    while True:
        counter += 1
        t1 = datetime.now()
        timediff = t1-t2
        avgtime = avgtime + (timediff.total_seconds())

        # Capture frames from both cameras
        
        left_frame = left_cam.capture_array()
        right_frame = right_cam.capture_array()
        left_frame = cv2.cvtColor(left_frame, cv2.COLOR_BGR2RGB)
        right_frame = cv2.cvtColor(right_frame, cv2.COLOR_BGR2RGB)

        # Combine frames side by side
        combined_frame = np.hstack((left_frame, right_frame))
        
        # Resize if needed
        if scale_ratio != 1.0:
            combined_frame = cv2.resize(combined_frame, (img_width*2, img_height))

        cv2.imshow("Stereo Pair", combined_frame)
        key = cv2.waitKey(1) & 0xFF
        t2 = datetime.now()

        if key == ord("q"):
            avgtime = avgtime/counter
            print("Average time between frames: " + str(avgtime))
            print("Average FPS: " + str(1/avgtime))
            if not os.path.isdir("./scenes"):
                os.makedirs("./scenes")
            cv2.imwrite(filename, combined_frame)
            break

finally:
    # Clean up
    left_cam.stop()
    right_cam.stop()
    cv2.destroyAllWindows()


