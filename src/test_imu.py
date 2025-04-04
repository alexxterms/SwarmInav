from unavlib import MSPy
from unavlib.modules import inavutil
from unavlib.modules.fast_functions import fastMSP

serial_port = "/dev/ttyUSB0"  # Change if needed
baudrate = 115200

with MSPy(device=serial_port, baudrate=baudrate) as board:
    imu_data = board.fast_read_imu()
    
    print("IMU Data:", imu_data)
