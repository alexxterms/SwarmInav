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

            # Print raw and processed data
            print(f"📡 Raw IMU Data: {raw_accel}")
            print(f"📡 Processed Accelerometer (G): {accel}")
            print(f"📡 Processed Gyroscope (deg/sec): {gyro}")
            print(f"📡 Magnetometer: {mag}")
            print("-" * 50)

            # Orientation Logic
            if accel[0] > 0.5:
                print("↩️ Tilting LEFT (Left Wing Down)")
            elif accel[0] < -0.5:
                print("↪️ Tilting RIGHT (Right Wing Down)")

            if accel[1] > 0.5:
                print("⬆️ Nose UP")
            elif accel[1] < -0.5:
                print("⬇️ Nose DOWN")

            if accel[2] > 0.8:
                print("🚀 Upright (Normal Level Flight)")
            elif accel[2] < 0.3:
                print("🛬 Laying Flat or Inverted")

            print("=" * 50)

        time.sleep(0.2)  # Adjust update rate if needed (200ms)
