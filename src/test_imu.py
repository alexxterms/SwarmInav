from yamspy import MSPy

serial_port = "/dev/ttyACM2"

with MSPy(device=serial_port, loglevel='DEBUG', baudrate=115200) as board:
    board.fast_read_imu()

    print("📡 IMU Data:")
    print("📡 Processed IMU Data:")
    print(f"Accelerometer (G): {[x / 512 for x in board.SENSOR_DATA['accelerometer']]}")
    print(f"Gyroscope (deg/sec): {[x * (4 / 16.4) for x in board.SENSOR_DATA['gyroscope']]}")
    print(f"Magnetometer: {board.SENSOR_DATA['magnetometer']}")  # Usually raw

