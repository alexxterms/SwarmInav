import time
import struct
from yamspy import MSPy

# Serial connection parameters
SERIAL_PORT = "/dev/ttyACM2"
BAUDRATE = 115200

# Connect to the flight controller
board = MSPy(device=SERIAL_PORT, baudrate=BAUDRATE)

if board.connect(trials=3):  
    print("✅ Serial port connected successfully")
else:
    raise Exception("❌ Failed to open serial port")

def read_imu():
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

def send_rc_command(channels):
    """Sends RC commands to the flight controller."""
    try:
        if len(channels) != 8:
            raise ValueError("RC command must contain 8 values.")
        board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_RAW_RC'], struct.pack('<8H', *channels))
    except Exception as e:
        print(f"Error sending RC command: {e}")

# Main loop
while True:
    try:
        # Read IMU data
        raw_imu_data = read_imu()
        if raw_imu_data:
            print("IMU Data:", raw_imu_data)

        # Example: Sending RC command (8 channels, placeholder values)
        channels = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
        send_rc_command(channels)

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(0.1)  # Adjust update rate if needed (100ms)
