import time
import struct
import serial
from yamspy import MSPy

class FlightController:
    def __init__(self, serial_port="/dev/ttyACM2", baudrate=115200):
        try:
            self.serial_port = serial_port
            self.baudrate = baudrate

            # Check if the port is already in use
            self.ser = serial.Serial(serial_port, baudrate, timeout=1)
            self.ser.close()  # Close immediately to allow MSPy to open it properly

            # Initialize MSPy
            self.board = MSPy(device=serial_port, loglevel='DEBUG', baudrate=baudrate)
            
            self.imu_data = {
                "accelerometer": [0, 0, 0],
                "gyroscope": [0, 0, 0],
                "magnetometer": [0, 0, 0]
            }
        except serial.SerialException as e:
            print(f"❌ ERROR: Could not open serial port {serial_port}. Make sure it's correct and not in use.")
            raise e
    
    def get_imu_data(self):
        """Requests and reads raw IMU data from the flight controller."""
        if self.board.send_RAW_msg(MSPy.MSPCodes['MSP_RAW_IMU']):
            data_length = 18
            msg = self.board.receive_raw_msg(size=(6+data_length))[5:]
            converted_msg = struct.unpack('<%dh' % (data_length // 2), msg[:-1])

            # Scale Accelerometer values (convert to G-force)
            acc_x, acc_y, acc_z = [val / 512.0 for val in converted_msg[:3]]
            
            # Scale Gyroscope values (convert to degrees/sec)
            gyro_x, gyro_y, gyro_z = [val * (4.0 / 16.4) for val in converted_msg[3:6]]
            
            # Magnetometer raw values
            mag_x, mag_y, mag_z = converted_msg[6:9]
            
            self.imu_data = {
                "accelerometer": [acc_x, acc_y, acc_z],
                "gyroscope": [gyro_x, gyro_y, gyro_z],
                "magnetometer": [mag_x, mag_y, mag_z]
            }
        return self.imu_data
    
    def send_rc_command(self, channels):
        """Sends RC commands to the flight controller."""
        if len(channels) != 8:
            raise ValueError("RC command must contain 8 values.")
        self.board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_RAW_RC'], struct.pack('<8H', *channels))
    
    def close(self):
        """Closes the serial connection."""
        if self.board.ser.is_open:
            self.board.ser.close()
            print("🔌 Serial port closed.")

