import time
import struct
from yamspy import MSPy
from imu_func import scale_imu_data, determine_orientation

class FlightController:
    def __init__(self, serial_port="/dev/ttyACM2", baudrate=115200):
        self.serial_port = serial_port
        self.baudrate = baudrate

    def read_imu(self):
        """Fetches raw IMU data from the flight controller."""
        try:
            with MSPy(device=self.serial_port, baudrate=self.baudrate) as board:
                if board.send_RAW_msg(MSPy.MSPCodes['MSP_RAW_IMU']):
                    dataHandler = board.receive_msg()
                    board.process_recv_data(dataHandler)  # Updates SENSOR_DATA

                    return {
                        "accelerometer": board.SENSOR_DATA['accelerometer'],
                        "gyroscope": board.SENSOR_DATA['gyroscope'],
                        "magnetometer": board.SENSOR_DATA['magnetometer']
                    }

        except Exception as e:
            print(f"Error reading IMU data: {e}")
            return None

    def send_rc_command(self, channels):
        """Sends RC commands to the flight controller."""
        try:
            with MSPy(device=self.serial_port, loglevel='DEBUG', baudrate=self.baudrate) as board:
                if len(channels) != 8:
                    raise ValueError("RC command must contain 8 values.")
                board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_RAW_RC'], struct.pack('<8H', *channels))

        except Exception as e:
            print(f"Error sending RC command: {e}")

# Example usage
fc = FlightController()

while True:
    try:
        raw_imu_data = fc.read_imu()
        if raw_imu_data:
            scaled_data = scale_imu_data(raw_imu_data)
            orientation = determine_orientation(scaled_data)

            print("IMU Data:", scaled_data)
            print("Orientation:", ", ".join(orientation))

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(0.1)  # Adjust update rate if needed (100ms)
