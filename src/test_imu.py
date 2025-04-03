from yamspy import MSPy

serial_port = "/dev/ttyACM2"

with MSPy(device=serial_port, loglevel='DEBUG', baudrate=115200) as board:
    board.fast_read_imu()

    print("📡 IMU Data:")
    print(f"Accelerometer: {board.SENSOR_DATA['accelerometer']}")
    print(f"Gyroscope: {board.SENSOR_DATA['gyroscope']}")
    print(f"Magnetometer: {board.SENSOR_DATA['magnetometer']}")
