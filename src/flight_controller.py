import time
import struct
from yamspy import MSPy

imu_port = "/dev/ttyACM3"  # First UART for IMU
rc_port = "/dev/ttyUSB0"   # Second UART for RC
baudrate = 115200

with MSPy(device=imu_port, baudrate=baudrate) as imu_board, MSPy(device=rc_port, baudrate=baudrate) as rc_board:
    if imu_board.connect(trials=3) and rc_board.connect(trials=3):
        print("✅ Both UARTs connected successfully")
    else:
        raise Exception("❌ Failed to connect to one or both serial ports")

    imu_interval = 0.02   # 50Hz (every 20 ms)
    rc_interval = 0.05    # 20Hz (every 50 ms)

    last_imu_time = time.time()
    last_rc_time = time.time()

    while True:
        current_time = time.time()

        # Read IMU data
        if current_time - last_imu_time >= imu_interval:
            if imu_board.send_RAW_msg(MSPy.MSPCodes['MSP_RAW_IMU']):
                dataHandler = imu_board.receive_msg()
                imu_board.process_recv_data(dataHandler)
                imu = imu_board.SENSOR_DATA['accelerometer']
                print("IMU:", imu)
            last_imu_time = current_time

        # Send RC command
        if current_time - last_rc_time >= rc_interval:
            rc_values = [1500] * 8  # Replace with your logic
            rc_board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_RAW_RC'], struct.pack('<8H', *rc_values))
            print("RC sent")
            last_rc_time = current_time
