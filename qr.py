import picamera2
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np

# Initialize the camera
camera = picamera2.Picamera2()
camera.start_preview()

def decode_qr(frame):
    """Decodes QR codes in a frame."""
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        qr_data = barcode.data.decode("utf-8")
        return qr_data

while True:
    # Capture a frame from the camera
    frame = camera.capture_array()

    # Convert the frame to RGB (OpenCV uses BGR by default)
    frame = frame[:, :, ::-1]

    # Resize the frame if needed
    # frame = cv2.resize(frame, (640, 480))  # adjust resolution if needed

    # Draw a bounding box around the detected QR code (optional)
    qr_data = decode_qr(frame)
    if qr_data:
        (x, y, w, h) = pyzbar.decode(frame)[0].rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame with QR code info (if any)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, f"QR Code: {qr_data or ''}", (10, 30), font, 1, (0, 255, 0), 2)

    # Show the camera feed
    cv2.imshow("QR Code Reader", frame)

    # Check for key press (to exit)
    if cv2.waitKey(1) == ord("q"):
        break

# Clean up
camera.stop_preview()
cv2.destroyAllWindows()
