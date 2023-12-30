from picamera import PiCamera
from time import sleep

# Initialize PiCamera
camera = PiCamera()

try:
    # Set camera resolution (adjust as needed)
    camera.resolution = (1280, 720)

    # Start preview for 5 seconds
    camera.start_preview()
    sleep(5)

    # Capture an image
    camera.capture('/home/pi/image.jpg')  # Replace '/home/pi/image.jpg' with your desired file path and name

    # Stop preview
    camera.stop_preview()

finally:
    # Release resources
    camera.close()
