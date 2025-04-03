import time
import struct
from yamspy import MSPy

# UART Configuration
imu_port = "/dev/ttyACM3"  # IMU on UART0
rc_port = "/dev/ttyUSB0"   # RC control on UART1
baudrate = 115200

# Scaling function (Example values, adjust as needed)
def scale_imu_data(raw_data):
    return {
        "accelerometer": [x / 2048.0 for x in raw_data["accelerometer"]],  # Convert to g-force
        "gyroscope": [x / 16.4 for x in raw_data["gyroscope"]],  # Convert to deg/sec
        "magnetometer": raw_data["magnetometer"]  # Keeping raw for now
    }

# Orientation determination
def determine_orientation(scaled_data):
    ax, ay, az = scaled_data["accelerometer"]
    gx, gy, gz = scaled_data["gyroscope"]

    orientation = []

    if ax > 0.5:
        orientation.append("Pitch Up")
    elif ax < -0.5:
        orientation.append("Pitch Down")

    if ay > 0.5:
        orientation.append("Roll Right")
    elif ay < -0.5:
        orientation.append("Roll Left")

    if gz > 30:
        orientation.append("Yaw Right")
    elif gz < -30:
        orientation.append("Yaw Left")

    return orientation if orientation else ["Stable"]

# Open connections using "with" to ensure proper handling
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

                raw_imu = {
                    "accelerometer": imu_board.SENSOR_DATA["accelerometer"],
                    "gyroscope": imu_board.SENSOR_DATA["gyroscope"],
                    "magnetometer": imu_board.SENSOR_DATA["magnetometer"]
                }

                scaled_imu = scale_imu_data(raw_imu)
                orientation = determine_orientation(scaled_imu)

                print("IMU:", scaled_imu)
                print("Orientation:", ", ".join(orientation))

            last_imu_time = current_time

        # Send RC command
        if current_time - last_rc_time >= rc_interval:
            rc_values = [1500] * 8  # Replace with actual logic
            rc_board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_RAW_RC'], struct.pack('<8H', *rc_values))
            
            last_rc_time = current_time
