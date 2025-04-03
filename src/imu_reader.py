from flight_controller import FlightController

fc = FlightController("/dev/ttyACM1")  
imu_data = fc.read_imu()  
print(imu_data)  

