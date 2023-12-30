import picamera2
import pyzbar.pyzbar as pyzbar
import cv2

# Initialize camera
camera = picamera2.Picamera2()

# Configure camera settings
camera.configure(
    resolution=(640, 480),  # Adjust resolution as needed
    framerate=30,          # Adjust framerate as desired
)

# Start preview
camera.start_preview(fullscreen=False, window=(100, 100, 640, 480))  # Adjust window position if needed

while True:
    # Capture a frame
    frame = camera.capture_array()

    # Convert frame to OpenCV format
    frame_opencv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # picamera2 uses BGR format

    # Decode QR codes
    decodedObjects = pyzbar.decode(frame_opencv)

    # Process decoded QR codes
    for obj in decodedObjects:
        data = obj.data.decode("utf-8")
        print("QR Code Data:", data)

    # Display live feed
    cv2.imshow("QR Code Scanner", frame_opencv)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop preview and close windows
camera.stop_preview()
cv2.destroyAllWindows()
