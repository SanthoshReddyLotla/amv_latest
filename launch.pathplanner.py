from rplidar import RPLidar
import serial
import time
import math
import matplotlib.pyplot as plt
from picamera import PiCamera
from picamera.array import PiRGBArray
from pyzbar.pyzbar import decode
import cv2

# Constants (replace with your values)
wheel_diameter = 10  # Replace with your wheel diameter in centimeters
encoder_pulses_per_rotation = 1000  # Replace with your encoder pulses per rotation

# Initialize serial connection to Arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Change port as needed

# Function to read encoder data
def read_encoder_data():
    left_data = ser.readline().decode().strip()
    right_data = ser.readline().decode().strip()
    return int(left_data) if left_data else None, int(right_data) if right_data else None

# Function to calculate distance based on encoder pulses
def calculate_distance(pulses):
    rotations = pulses / encoder_pulses_per_rotation
    distance = rotations * (wheel_diameter * math.pi)
    return distance

# Function to scan QR codes using the PiCamera
def scan_qr_code():
    camera = PiCamera()
    camera.resolution = (640, 480)
    raw_capture = PiRGBArray(camera)

    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array

        # Convert image to grayscale for QR code detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Decode QR codes
        decoded_objects = decode(gray)

        # Process detected QR codes
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            print(f"QR Code Data: {qr_data}")
            # You can perform actions based on the QR data here

        # Clear the stream in preparation for the next frame
        raw_capture.truncate(0)

        # You might want to add logic to handle when to stop scanning

    # Release resources
    camera.close()

# Function for obstacle avoidance using RPLidar and encoder data
def obstacle_avoidance(lidar):
    try:
        # Initialize variables for encoder readings and distance traveled
        prev_left_encoder = 0
        prev_right_encoder = 0
        total_distance = 0

        while True:
            # Read encoder data for left and right wheels
            left_encoder, right_encoder = read_encoder_data()

            if left_encoder is not None and right_encoder is not None:
                # Calculate distance traveled by both wheels
                left_distance = calculate_distance(left_encoder - prev_left_encoder)
                right_distance = calculate_distance(right_encoder - prev_right_encoder)

                # Update total distance traveled
                total_distance += (left_distance + right_distance) / 2  # Average distance covered by both wheels
                prev_left_encoder = left_encoder
                prev_right_encoder = right_encoder

                # Display encoder readings and total distance traveled
                print(f"Left Encoder: {left_encoder}, Right Encoder: {right_encoder}")
                print(f"Total Distance Traveled: {total_distance:.2f} cm")

            # Rest of your obstacle avoidance logic goes here
            # You can integrate the lidar data and use the total_distance variable for navigation decisions

            # Example:
            # scan_data = lidar.iter_scans(10)  # Get lidar scan data for 10 iterations
            # filtered_distance = filter_front_distance(scan_data)
            # if filtered_distance is not None and filtered_distance < threshold_distance:
            #     # Implement obstacle avoidance maneuver here based on lidar data and traveled distance

    except Exception as e:
        print(f"An error occurred: {e}")

# Main function to orchestrate the process
def main():
    try:
        lidar = RPLidar('/dev/ttyUSB0')  # Change port as needed
        time.sleep(2)  # Allow time to connect to the RPLIDAR

        # Start obstacle avoidance and QR code scanning in separate threads or processes
        # Example using threads (you might want to use proper threading or multiprocessing)
        obstacle_thread = threading.Thread(target=obstacle_avoidance, args=(lidar,))
        qr_thread = threading.Thread(target=scan_qr_code)

        obstacle_thread.start()
        qr_thread.start()

        obstacle_thread.join()
        qr_thread.join()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
