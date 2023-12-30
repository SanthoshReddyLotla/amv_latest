import picamera2
import cv2
import pyzbar.pyzbar as pyzbar

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

    # Decode QR codes in the frame
    qr_data = decode_qr(frame)

    if qr_data:
        print("QR code value:", qr_data)
        break  # Exit the loop after successfully reading a QR code

    # Display the frame (optional for debugging)
    cv2.imshow("QR Code Reader", frame)

    # Check for key press (to exit)
    if cv2.waitKey(1) == ord("q"):
        break

# Clean up
camera.stop_preview()
cv2.destroyAllWindows()
