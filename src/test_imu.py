import time
import math
from yamspy import MSPy

serial_port = "/dev/ttyACM1"

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

            # Compute Roll & Pitch angles
            roll_angle = math.degrees(math.atan2(accel[1], accel[2]))  # Left/Right Tilt
            pitch_angle = math.degrees(math.atan2(accel[0], math.sqrt(accel[1]**2 + accel[2]**2)))  # Nose Up/Down FIXED

            # Determine orientation
            orientation = []

            if pitch_angle > 10:
                orientation.append("Nose Down")  # FIXED
            elif pitch_angle < -10:
                orientation.append("Nose Up")  # FIXED

            if roll_angle > 10:
                orientation.append("Right Wing Down")
            elif roll_angle < -10:
                orientation.append("Left Wing Down")

            if gyro[2] > 5:
                orientation.append("Turning Right")
            elif gyro[2] < -5:
                orientation.append("Turning Left")

            if accel[2] > 1.1:
                orientation.append("Climbing")
            elif accel[2] < 0.9:
                orientation.append("Descending")

            if not orientation:
                orientation.append("Level Flight")

            # Print processed values and orientation
            print(f"📡 Processed IMU Data:")
            print(f"Accelerometer (G): {accel}")
            print(f"Gyroscope (deg/sec): {gyro}")
            print(f"Magnetometer: {mag}")
            print(f"🛑 Orientation: {' | '.join(orientation)}")
            print("-" * 50)

        time.sleep(0.1)  # Adjust update rate if needed (100ms)
