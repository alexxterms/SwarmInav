import time
import math
from imu_func import scale_imu_data, determine_orientation
from yamspy import MSPy

class FlightController:
    def __init__(self, serial_port="/dev/ttyACM2", baudrate=115200):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.board = None  # MSPy board will be initialized in the context manager

    def read_imu(self):
        """Requests and reads raw IMU data from the flight controller."""
        try:
            with MSPy(device=self.serial_port, loglevel='DEBUG', baudrate=self.baudrate) as board:
                if board.send_RAW_msg(MSPy.MSPCodes['MSP_RAW_IMU']):
                    dataHandler = board.receive_msg()
                    board.process_recv_data(dataHandler)  # Ensures SENSOR_DATA is updated

                    # Retrieve raw IMU data
                    raw_accel = board.SENSOR_DATA['accelerometer']
                    raw_gyro = board.SENSOR_DATA['gyroscope']
                    raw_mag = board.SENSOR_DATA['magnetometer']

                    # Process Accelerometer (Convert to G-force)
                    acc_x, acc_y, acc_z = [val / 512.0 for val in raw_accel]

                    # Process Gyroscope (Convert to degrees/sec)
                    gyro_x = raw_gyro[0] * (4.0 / 16.4)
                    gyro_y = raw_gyro[1] * (4.0 / 16.4)
                    gyro_z = raw_gyro[2] * (4.0 / 16.4)

                    # Compute Roll & Pitch angles
                    roll_angle = math.degrees(math.atan2(acc_y, acc_z))
                    pitch_angle = math.degrees(math.atan2(acc_x, math.sqrt(acc_y**2 + acc_z**2)))

                    # Determine Orientation
                    orientation = []

                    if pitch_angle > 10:
                        orientation.append("Nose Up")
                    elif pitch_angle < -10:
                        orientation.append("Nose Down")

                    if roll_angle > 10:
                        orientation.append("Right Wing Down")
                    elif roll_angle < -10:
                        orientation.append("Left Wing Down")

                    if gyro_z < -5:
                        orientation.append("Turning Right")
                    elif gyro_z > 5:
                        orientation.append("Turning Left")

                    if acc_z > 1.1:
                        orientation.append("Climbing")
                    elif acc_z < 0.9:
                        orientation.append("Descending")

                    if not orientation:
                        orientation.append("Level Flight")

                    # Return Processed IMU Data
                    return {
                        "imu_data": {
                            "accelerometer": [acc_x, acc_y, acc_z],
                            "gyroscope": [gyro_x, gyro_y, gyro_z],
                            "magnetometer": raw_mag
                        },
                        "orientation": orientation
                    }

        except Exception as e:
            raise ValueError(f"Error reading IMU data: {e}")

    def send_rc_command(self, channels):
        """Sends RC commands to the flight controller."""
        try:
            with MSPy(device=self.serial_port, loglevel='DEBUG', baudrate=self.baudrate) as board:
                if len(channels) != 8:
                    raise ValueError("RC command must contain 8 values.")
                board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_RAW_RC'], struct.pack('<8H', *channels))
        except Exception as e:
            raise ValueError(f"Error sending RC command: {e}")

# Example of using the class
fc = FlightController()

while True:
    try:
        imu_data = fc.read_imu()
        scaled_data = scale_imu_data(imu_data["imu_data"])
        orientation = determine_orientation(scaled_data)

        print("IMU Data:", scaled_data)
        print("Orientation:", ", ".join(orientation))

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(0.1)
