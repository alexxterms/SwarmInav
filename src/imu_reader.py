"ALL THE FUNCTIONS RELATED TO IMU ARE IN THIS FILE"

import time
from flight_controller import FlightController

class IMUReader:
    def __init__(self, fc: FlightController):
        self.fc = fc

    def read_imu(self):
        imu_data = self.fc.read_imu()
        if imu_data:
            accel, gyro, mag, orientation = imu_data
            print(f"\U0001F4E1 Processed IMU Data:")
            print(f"Accelerometer (G): {accel}")
            print(f"Gyroscope (deg/sec): {gyro}")
            print(f"Magnetometer: {mag}")
            print(f"\U0001F4E1 Orientation: {orientation}")
            print("-" * 50)
        return imu_data

if __name__ == "__main__":
    fc = FlightController("/dev/ttyACM1")
    imu_reader = IMUReader(fc)
    
    while True:
        imu_reader.read_imu()
        time.sleep(0.1)


