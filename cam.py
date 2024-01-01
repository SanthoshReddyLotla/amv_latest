import io
import picamera
import zbarlight
from PIL import Image

def detect_qr_code(image_stream):
    # Convert the image stream to a PIL Image
    image = Image.open(image_stream)

    # Convert the image to grayscale
    gray_image = image.convert('L')

    # Detect QR codes in the grayscale image
    codes = zbarlight.scan_codes('qrcode', gray_image)
    return codes

def main():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        
        # Start a preview to display the live feed
        camera.start_preview()

        # Create a stream to capture images
        stream = io.BytesIO()

        for _ in camera.capture_continuous(stream, format='jpeg'):
            # Move to the beginning of the stream to read the captured image
            stream.seek(0)

            # Detect QR codes in the captured image
            codes = detect_qr_code(stream)
            
            if codes is not None:
                # If QR code is detected, display its value
                for code in codes:
                    print(f"Detected QR code: {code.decode('utf-8')}")

            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()

if __name__ == "__main__":
    main()
