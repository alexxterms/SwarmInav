import time
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

            # Convert accelerometer to Gs (assuming MPU6050, /512)
            accel = [val / 512 for val in raw_accel]

            # Convert gyroscope to degrees/sec (assuming *4/16.4 scaling)
            gyro = [val * (4 / 16.4) for val in raw_gyro]

            # Keep magnetometer raw for now
            mag = raw_mag  

            # Print raw data
            print(f"📡 Raw IMU Data:")
            print(f"Accelerometer (Raw): {raw_accel}")
            print(f"Gyroscope (Raw): {raw_gyro}")
            print(f"Magnetometer (Raw): {raw_mag}")
            print("-" * 50)

            # Print processed values
            print(f"📡 Processed IMU Data:")
            print(f"Accelerometer (G): {accel}")
            print(f"Gyroscope (deg/sec): {gyro}")
            print(f"Magnetometer: {mag}")
            print("-" * 50)

            # Expected orientation debugging
            if accel[0] > 0.5:
                print("↪️ Right Wing Down")
            elif accel[0] < -0.5:
                print("↩️ Left Wing Down")

            if accel[1] > 0.5:
                print("⬆️ Nose Down")
            elif accel[1] < -0.5:
                print("⬇️ Nose Up")

            if accel[2] > 0.8:
                print("🚀 Upright")
            elif accel[2] < 0.3:
                print("🛬 Laying Flat")

            print("=" * 50)

        time.sleep(0.2)  # Adjust update rate if needed (200ms)
