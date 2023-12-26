import cv2
from time import sleep
from pyzbar.pyzbar import decode

def capture_qr_codes():
    # Initialize the camera (if using the default camera index 0)
    camera = cv2.VideoCapture(0)

    cv2.namedWindow("Camera Feed")  # Create a window to show the camera feed

    frame_count = 0  # Variable to track captured frames

    try:
        while True:
            sleep(0.1)  # Adjust delay between captures as needed

            # Capture a frame from the camera
            ret, frame = camera.read()

            # Check if the frame was successfully captured
            if ret:
                cv2.imshow("Camera Feed", frame)  # Display the captured frame

                # Read the saved image and decode QR codes
                barcodes = decode(frame)
#test
                if barcodes:
                    for barcode in barcodes:
                        qr_data = barcode.data.decode('utf-8')
                        print(f"QR Code Data: {qr_data}")
                        # Perform actions based on the QR data here

                if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                    break

            else:
                print("Failed to capture frame.")

    finally:
        # Release the camera and destroy OpenCV windows
        camera.release()
        cv2.destroyAllWindows()

# Run the function to start capturing images and detecting QR codes
capture_qr_codes()
