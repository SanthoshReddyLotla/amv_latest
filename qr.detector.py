from time import sleep
from io import BytesIO
import picamera
from PIL import Image
from pyzbar.pyzbar import decode

def capture_qr_codes():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)  # Set the resolution according to your requirements
        sleep(2)  # Allow the camera to warm up

        try:
            stream = BytesIO()
            for _ in camera.capture_continuous(stream, format='jpeg'):
                stream.seek(0)  # Reset stream position to the beginning
                image = Image.open(stream)  # Open image using PIL

                # Convert PIL image to numpy array for decoding
                frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                # Decode QR codes
                barcodes = decode(frame)

                if barcodes:
                    for barcode in barcodes:
                        qr_data = barcode.data.decode('utf-8')
                        print(f"QR Code Data: {qr_data}")
                        # Perform actions based on the QR data here

                stream.seek(0)
                stream.truncate()

                # Adjust the delay between captures as needed
                sleep(0.1)

        except KeyboardInterrupt:
            pass
        finally:
            camera.close()

# Run the function to start capturing images and detecting QR codes
capture_qr_codes()
