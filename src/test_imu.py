

import time
from yamspy import MSPy

serial_port = "/dev/ttyACM0"

with MSPy(device=serial_port, loglevel='DEBUG', baudrate=115200) as board:
    while True:
        if board.send_RAW_msg(MSPy.MSPCodes['MSP_RAW_IMU']):
            dataHandler = board.receive_msg()
            board.process_recv_data(dataHandler)  # Ensures SENSOR_DATA is updated

            # Retrieve IMU data
            raw_accel = board.SENSOR_DATA['accelerometer']
            raw_gyro = board.SENSOR_DATA['gyroscope']
            raw_mag = board.SENSOR_DATA['magnetometer']

            # Process values
            accel = [val / 512 for val in raw_accel]  # Convert to G (assuming MPU6050)
            gyro = [val * (4 / 16.4) for val in raw_gyro]  # Convert to deg/sec
            mag = raw_mag  # Keeping raw (may need scaling)

            # Print processed values
            print(f"📡 Processed IMU Data:")
            print(f"Accelerometer (G): {accel}")
            print(f"Gyroscope (deg/sec): {gyro}")
            print(f"Magnetometer: {mag}")
            print("-" * 50)

        time.sleep(0.1)  # Adjust update rate if needed (100ms)
