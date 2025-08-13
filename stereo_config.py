from picamera2 import Picamera2
import libcamera

def init_stereo_cameras():
    # Initialize two cameras
    left_cam = Picamera2(0)  # First camera
    right_cam = Picamera2(1)  # Second camera
    
    # Configure both cameras with identical settings
    config = {
        "size": (1280, 720)
    }
    
    left_config = left_cam.create_still_configuration(raw=config)
    right_config = right_cam.create_still_configuration(raw=config)
    
    left_cam.configure(left_config)
    right_cam.configure(right_config)
    
    return left_cam, right_cam
