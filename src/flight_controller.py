import time
import struct
from yamspy import MSPy

class FlightController:
    def __init__(self, serial_port="/dev/ttyACM2", baudrate=115200):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.board = None  # To hold the board object

    def connect(self):
        """Connects to the flight controller."""
        try:
            with MSPy(device=self.serial_port, baudrate=self.baudrate) as board:
                if board.connect(trials=3):
                    print("✅ Serial port connected successfully")
                    self.board = board  # Store the board for later use
                else:
                    raise Exception("❌ Failed to open serial port")
        except Exception as e:
            print(f"Error connecting to FC: {e}")
            self.board = None

    def read_imu(self):
        """Fetches raw IMU data from the flight controller."""
        if self.board is None:
            print("❌ Board not connected!")
            return None
        
        try:
            if self.board.send_RAW_msg(MSPy.MSPCodes['MSP_RAW_IMU']):
                dataHandler = self.board.receive_msg()
                self.board.process_recv_data(dataHandler)  # Updates SENSOR_DATA

                return {
                    "accelerometer": self.board.SENSOR_DATA['accelerometer'],
                    "gyroscope": self.board.SENSOR_DATA['gyroscope'],
                    "magnetometer": self.board.SENSOR_DATA['magnetometer']
                }
        except Exception as e:
            print(f"Error reading IMU data: {e}")
            return None

    def send_rc_command(self, channels):
        """Sends RC commands to the flight controller."""
        if self.board is None:
            print("❌ Board not connected!")
            return
        
        try:
            if len(channels) != 8:
                raise ValueError("RC command must contain 8 values.")
            self.board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_RAW_RC'], struct.pack('<8H', *channels))
        except Exception as e:
            print(f"Error sending RC command: {e}")

# Example usage
fc = FlightController()

# Connect to FC once
fc.connect()

if fc.board:
    while True:
        try:
            # Read IMU data
            raw_imu_data = fc.read_imu()
            if raw_imu_data:
                # You can scale and process the IMU data here if needed
                print("IMU Data:", raw_imu_data)

            # Example: Sending RC command (8 channels, placeholder values)
            channels = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
            fc.send_rc_command(channels)

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(0.1)  # Adjust update rate if needed (100ms)
else:
    print("Failed to connect to FC.")
