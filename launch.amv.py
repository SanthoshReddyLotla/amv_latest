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

def obstacle_avoidance(lidar):
    try:
        for scan in lidar.iter_scans():
            plot_lidar_data(scan)  # Display live plot of Lidar data
            front_distance = filter_front_distance(scan)
            if front_distance is not None:
                print("Front distance:", front_distance)
                if front_distance < 1000:  # Distance threshold for obstacle detection
                    send_command('x')  # Stop the motors
                else:
                    send_command('w')  # Move forward
    except KeyboardInterrupt:
        print("Program interrupted by user")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    finally:
        lidar.stop()
        lidar.disconnect()
        ser.close()
        print("Connections closed")

def main():
    try:
        lidar = RPLidar('/dev/ttyUSB0')  # Change port as needed
        time.sleep(2)  # Allow time to connect to the RPLIDAR

        obstacle_avoidance(lidar)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
