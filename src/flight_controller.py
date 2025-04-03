import time
import struct
from yamspy import MSPy

class FlightController:
    def __init__(self, serial_port="/dev/ttyACM2", baudrate=115200):
        self.serial_port = serial_port
        self.baudrate = baudrate

    def connect(self):
        """Connects to the flight controller."""
        try:
            with MSPy(device=self.serial_port, baudrate=self.baudrate) as board:
                # Check if board is connected
                if board.connect(trials=3):
                    print("✅ Serial port connected successfully")
                    return board
                else:
                    raise Exception("❌ Failed to open serial port")
        except Exception as e:
            print(f"Error connecting to FC: {e}")
            return None

    def read_imu(self, board):
        """Fetches raw IMU data from the flight controller."""
        try:
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

    def send_rc_command(self, board, channels):
        """Sends RC commands to the flight controller."""
        try:
            if len(channels) != 8:
                raise ValueError("RC command must contain 8 values.")
            board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_RAW_RC'], struct.pack('<8H', *channels))
        except Exception as e:
            print(f"Error sending RC command: {e}")

# Example usage
fc = FlightController()

# Connect to FC once
board = fc.connect()

if board:
    while True:
        try:
            # Read IMU data
            raw_imu_data = fc.read_imu(board)
            if raw_imu_data:
                # You can scale and process the IMU data here if needed
                print("IMU Data:", raw_imu_data)

            # Example: Sending RC command (8 channels, placeholder values)
            channels = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
            fc.send_rc_command(board, channels)

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(0.1)  # Adjust update rate if needed (100ms)
else:
    print("Failed to connect to FC.")
