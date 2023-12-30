from time import sleep
import numpy as np
import cv2
from PIL import Image
from pyzbar.pyzbar import decode
from picamera.array import PiRGBArray
from picamera import PiCamera

def capture_qr_codes():
    with PiCamera() as camera:
        camera.resolution = (640, 480)  # Set the resolution according to your requirements
        camera.framerate = 24  # Set the frame rate (adjust as needed)
        raw_capture = PiRGBArray(camera, size=camera.resolution)

        sleep(2)  # Allow the camera to warm up

        try:
            for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
                image = frame.array

                # Convert to grayscale for decoding
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Decode QR codes
                barcodes = decode(gray)

                if barcodes:
                    for barcode in barcodes:
                        qr_data = barcode.data.decode('utf-8')
                        print(f"QR Code Data: {qr_data}")
                        # Perform actions based on the QR data here

                raw_capture.truncate(0)  # Clear the stream in preparation for the next frame

                # Adjust the delay between captures as needed
                sleep(0.1)

        except KeyboardInterrupt:
            pass

# Run the function to start capturing images and detecting QR codes
capture_qr_codes()
