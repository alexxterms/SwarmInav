from flight_controller import FlightController
from imu_reader import IMUReader
import time

fc = FlightController("/dev/ttyACM2")  # Create only ONE instance
imu_reader = IMUReader(fc)  # Pass the same instance

while True:
    imu_reader.read_imu()  # Reads IMU without opening serial port again
    time.sleep(0.1)

