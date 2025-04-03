import time
import struct
import threading
from yamspy import MSPy
from imu_func import scale_imu_data, determine_orientation

SERIAL_PORT = "/dev/ttyACM2"
BAUDRATE = 115200

# Establish connection
with MSPy(device=SERIAL_PORT, baudrate=BAUDRATE) as board:
    if board.connect(trials=3):
        print("✅ Serial port connected successfully")
    else:
        raise Exception("❌ Failed to open serial port")

    # Function to read and process IMU data
    def read_imu_loop():
        while True:
            try:
                if board.send_RAW_msg(MSPy.MSPCodes['MSP_RAW_IMU']):
                    dataHandler = board.receive_msg()
                    board.process_recv_data(dataHandler)

                    raw_imu_data = {
                        "accelerometer": board.SENSOR_DATA['accelerometer'],
                        "gyroscope": board.SENSOR_DATA['gyroscope'],
                        "magnetometer": board.SENSOR_DATA['magnetometer']
                    }

                    # Scale IMU data
                    scaled_data = scale_imu_data(raw_imu_data)

                    # Determine orientation
                    orientation = determine_orientation(scaled_data)

                    print("IMU Data:", scaled_data)
                    print("Orientation:", ", ".join(orientation))
                    
            except Exception as e:
                print(f"Error reading IMU data: {e}")
            
            time.sleep(0.1)  # Adjust rate if needed

    # Function to send RC commands
    def send_rc_loop():
        while True:
            try:
                channels = [1500] * 8  # Example RC values
                board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_RAW_RC'], struct.pack('<8H', *channels))
            except Exception as e:
                print(f"Error sending RC command: {e}")
            
            time.sleep(0.1)  # Adjust rate if needed

    # Start both tasks in separate threads
    imu_thread = threading.Thread(target=read_imu_loop)
    rc_thread = threading.Thread(target=send_rc_loop)

    imu_thread.start()
    rc_thread.start()

    imu_thread.join()
    rc_thread.join()
