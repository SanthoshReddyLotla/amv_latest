import cv2
from picamera import PiCamera
from pyzbar import pyzbar

def detect_qr_codes(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect QR codes in the frame
    barcodes = pyzbar.decode(gray)

    # Process detected QR codes
    for barcode in barcodes:
        # Extract QR code data and draw a rectangle around it
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        barcode_data = barcode.data.decode("utf-8")
        cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Return the QR code data
        return barcode_data

    # If no QR code is detected, return None
    return None

# Initialize PiCamera
camera = PiCamera()

# Set camera resolution (adjust as needed)
camera.resolution = (640, 480)

# Initialize OpenCV window
cv2.namedWindow("QR Code Reader")

try:
    while True:
        # Capture a frame from the camera
        frame = camera.capture_continuous(rawCapture, format="bgr")
        frame = frame.array

        # Detect QR codes in the frame
        qr_data = detect_qr_codes(frame)

        # Display the frame with detected QR codes
        cv2.imshow("QR Code Reader", frame)

        # If QR code is detected, print the data
        if qr_data:
            print("Detected QR code:", qr_data)

        # Check for the 'q' key to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Release resources
    cv2.destroyAllWindows()
    camera.close()
