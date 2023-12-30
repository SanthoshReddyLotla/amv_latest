import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Decode the QR code
    decodedObjects = pyzbar.decode(frame)

    # Display the result
    for obj in decodedObjects:
        print("QR Code Value: ", obj.data)

    # Exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
