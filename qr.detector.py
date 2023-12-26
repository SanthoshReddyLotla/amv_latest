from picamera import PiCamera
from time import sleep
import cv2
from pyzbar.pyzbar import decode

def capture_qr_codes():
    camera = PiCamera()
    camera.resolution = (640, 480)

    try:
        while True:
            sleep(2)  # Adjust delay between captures as needed

            # Capture an image using the PiCamera
            camera.capture('image.jpg')  # Save the image

            # Read the saved image and decode QR codes
            image = cv2.imread('image.jpg')
            barcodes = decode(image)

            if barcodes:
                for barcode in barcodes:
                    qr_data = barcode.data.decode('utf-8')
                    print(f"QR Code Data: {qr_data}")
                    # Perform actions based on the QR data here

            else:
                print("No QR code detected.")

    finally:
        camera.close()

# Run the function to start capturing images and detecting QR codes
capture_qr_codes()
