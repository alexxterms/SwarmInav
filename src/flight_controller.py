import time
import struct
from yamspy import MSPy

# Setup
serial_port = "/dev/ttyACM0"
baudrate = 115200

with MSPy(device=serial_port, baudrate=baudrate) as board:
    if board.connect(trials=3):
        print("✅ Serial port connected")
    else:
        raise Exception("❌ Failed to connect")

    imu_interval = 0.02   # 50Hz (every 20 ms)
    rc_interval = 0.05    # 20Hz (every 50 ms)

    last_imu_time = time.time()
    last_rc_time = time.time()

    while True:
        current_time = time.time()

        # Read IMU data
        if current_time - last_imu_time >= imu_interval:
            if board.send_RAW_msg(MSPy.MSPCodes['MSP_RAW_IMU']):
                dataHandler = board.receive_msg()
                board.process_recv_data(dataHandler)
                imu = board.SENSOR_DATA['accelerometer']
                print("IMU:", imu)
            last_imu_time = current_time

        # Send RC command
        if current_time - last_rc_time >= rc_interval:
            rc_values = [1500] * 8  # Replace with your logic
            board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_RAW_RC'], struct.pack('<8H', *rc_values))
            print("RC sent")
            last_rc_time = current_time
