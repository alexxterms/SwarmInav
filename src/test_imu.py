import time
import math
from yamspy import MSPy

serial_port = "/dev/ttyACM1"

with MSPy(device=serial_port, loglevel='DEBUG', baudrate=115200) as board:
    while True:
        if board.send_RAW_msg(MSPy.MSPCodes['MSP_RAW_IMU']):
            dataHandler = board.receive_msg()
            board.process_recv_data(dataHandler)  # Ensures SENSOR_DATA is updated

            # Retrieve raw IMU data
            raw_accel = board.SENSOR_DATA['accelerometer']
            raw_gyro = board.SENSOR_DATA['gyroscope']
            raw_mag = board.SENSOR_DATA['magnetometer']

            # Process Accelerometer (Convert to G-force)
            acc_x, acc_y, acc_z = [val / 512.0 for val in raw_accel]

            # Process Gyroscope (Convert to degrees/sec)
            gyro_x = raw_gyro[0] * (4.0 / 16.4)
            gyro_y = raw_gyro[1] * (4.0 / 16.4)
            gyro_z = raw_gyro[2] * (4.0 / 16.4)

            # Compute Roll & Pitch angles
            roll_angle = math.degrees(math.atan2(acc_y, acc_z))
            pitch_angle = math.degrees(math.atan2(-acc_x, math.sqrt(acc_y**2 + acc_z**2)))

            # Determine Orientation
            orientation = []

            if pitch_angle > 10:
                orientation.append("Nose Up")
            elif pitch_angle < -10:
                orientation.append("Nose Down")

            if roll_angle > 10:
                orientation.append("Right Wing Down")
            elif roll_angle < -10:
                orientation.append("Left Wing Down")

            if gyro_z > 5:
                orientation.append("Turning Right")
            elif gyro_z < -5:
                orientation.append("Turning Left")

            if acc_z > 1.1:
                orientation.append("Climbing")
            elif acc_z < 0.9:
                orientation.append("Descending")

            if not orientation:
                orientation.append("Level Flight")

            # Print Processed IMU Data
            print("📡 Processed IMU Data:")
            print(f"Accelerometer (G): [{acc_x:.3f}, {acc_y:.3f}, {acc_z:.3f}]")
            print(f"Gyroscope (deg/sec): [{gyro_x:.3f}, {gyro_y:.3f}, {gyro_z:.3f}]")
            print(f"Magnetometer: {raw_mag}")
            print(f"📡 Orientation: {', '.join(orientation)}")
            print("-" * 50)

        time.sleep(0.1)  # Adjust update rate if needed (100ms)
