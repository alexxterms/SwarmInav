"ALL THE FUNCTIONS RELATED TO IMU ARE IN THIS FILE"

import time

def read_imu_continuous(fc):
    """Continuously reads IMU data from the flight controller."""
    try:
        while True:
            imu_data = fc.read_imu()
            if imu_data:
                acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = imu_data
                print(f"📡 IMU - Acc: ({acc_x}, {acc_y}, {acc_z}) | Gyro: ({gyro_x}, {gyro_y}, {gyro_z})")
            time.sleep(0.1)  # Adjust as needed
    except KeyboardInterrupt:
        print("⏹️ Stopping IMU readings.")

