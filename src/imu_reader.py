import time
import math
from flight_controller import FlightController

class IMUReader:
    def __init__(self, fc: FlightController):
       
        self.fc = fc

    def read_imu(self):
        imu_data = self.fc.get_imu_data()
        if imu_data:
            accel, gyro, mag = imu_data["accelerometer"], imu_data["gyroscope"], imu_data["magnetometer"]
            
            # Compute Roll & Pitch angles from accelerometer
            roll_angle = math.degrees(math.atan2(accel[1], accel[2]))
            pitch_angle = math.degrees(math.atan2(-accel[0], math.sqrt(accel[1]**2 + accel[2]**2)))
            
            # Determine orientation based on angles
            orientation = []

            if pitch_angle > 10:
                orientation.append("Nose Up")
            elif pitch_angle < -10:
                orientation.append("Nose Down")

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
            
            print(f"\U0001F4E1 Processed IMU Data:")
            print(f"Accelerometer (G): {accel}")
            print(f"Gyroscope (deg/sec): {gyro}")
            print(f"Magnetometer: {mag}")
            print(f"\U0001F4E1 Orientation: {', '.join(orientation)}")
            print("-" * 50)
        return imu_data

