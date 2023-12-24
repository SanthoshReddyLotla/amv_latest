from rplidar import RPLidar
import serial
import time
import math
import matplotlib.pyplot as plt

# Initialize serial connection to Arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Change port as needed

def send_command(cmd):
    ser.write(cmd.encode())

def filter_front_distance(scan_data):
    front_data = [item[2] for item in scan_data if (0 <= item[1] <= 30) or (330 <= item[1] <= 360)]
    if front_data:
        return min(front_data)
    else:
        return None

def plot_lidar_data(scan_data):
    angles = [item[1] for item in scan_data]
    distances = [item[2] for item in scan_data]

    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, projection='polar')
    ax.plot(angles, distances, 'b.', alpha=0.75)
    ax.set_rmax(4000)  # Set maximum distance for the plot
    plt.title('RPLidar Data')
    plt.show()

def read_encoder_data():
    # Read encoder data via serial port and return the readings
    # Example:
    # left_data = ser.readline().decode().strip()
    # right_data = ser.readline().decode().strip()
    # return int(left_data) if left_data else None, int(right_data) if right_data else None
    pass  # Replace with your implementation

def calculate_distance(pulses):
    rotations = pulses / encoder_pulses_per_rotation
    distance = rotations * (wheel_diameter * math.pi)
    return distance

def obstacle_avoidance(lidar):
    try:
        # Existing code remains unchanged

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

    except Exception as e:
        print(f"An error occurred: {e}")

# Constants
wheel_diameter = 10  # Replace with your wheel diameter in centimeters
encoder_pulses_per_rotation = 1000  # Replace with your encoder pulses per rotation

def main():
    try:
        lidar = RPLidar('/dev/ttyUSB0')  # Change port as needed
        time.sleep(2)  # Allow time to connect to the RPLIDAR

        obstacle_avoidance(lidar)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
