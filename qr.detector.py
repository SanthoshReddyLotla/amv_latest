import cv2
from time import sleep
from pyzbar.pyzbar import decode

def capture_qr_codes():
    # Initialize the camera (if using the default camera index 0)
    camera = cv2.VideoCapture(0)

    try:
        while True:
            sleep(2)  # Adjust delay between captures as needed

            # Capture a frame from the camera
            ret, frame = camera.read()

            # Check if the frame was successfully captured
            if ret:
                cv2.imwrite('image.jpg', frame)  # Save the captured frame as an image

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
            else:
                print("Failed to capture frame.")

    finally:
        # Release the camera
        camera.release()

# Run the function to start capturing images and detecting QR codes
capture_qr_codes()
