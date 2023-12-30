import time
import numpy as np
import cv2
from pyzbar.pyzbar import decode
import picamera2

def capture_qr_codes():
    with picamera2.Picamera2() as camera:
        camera.configure(
            resolution=(640, 480),  # Set the resolution
            framerate=24,          # Set the frame rate
            format="rgb"           # Specify RGB format
        )

        sleep(2)  # Allow the camera to warm up

        try:
            for frame in camera.capture_continuous(output_format="rgb"):
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

        except KeyboardInterrupt:
            pass

# Run the function to start capturing images and detecting QR codes
capture_qr_codes()
