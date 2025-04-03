import time
import struct
from yamspy import MSPy
from imu_func import scale_imu_data, determine_orientation  # ✅ Import processing functions

class FlightController:
    def __init__(self, serial_port="/dev/ttyACM2", baudrate=115200):
        self.board = MSPy(device=serial_port, loglevel='DEBUG', baudrate=baudrate)

        # ✅ Attempt to open the serial port if not already open
        if not self.board.ser.is_open:
            try:
                self.board.ser.open()  # Manually opening the serial port
                print("Serial port opened successfully.")
            except Exception as e:
                raise ConnectionError(f"Failed to open serial port: {e}")

    def read_imu(self):
        """Requests and reads raw IMU data from the flight controller."""
        # Ensure serial is open before trying to send/receive
        if not self.board.ser.is_open:
            raise ConnectionError("Serial port is not open!")

        try:
            if self.board.send_RAW_msg(MSPy.MSPCodes['MSP_RAW_IMU']):
                data_length = 18
                msg = self.board.receive_raw_msg(size=(6+data_length))

                if msg:
                    msg = msg[5:]  # Extract the data part
                    converted_msg = struct.unpack('<%dh' % (data_length // 2), msg[:-1])

                    return {
                        "accelerometer": converted_msg[:3],
                        "gyroscope": converted_msg[3:6],
                        "magnetometer": converted_msg[6:9]
                    }
                else:
                    raise ValueError("Failed to receive valid IMU data.")
        except Exception as e:
            raise ValueError(f"Error reading IMU data: {e}")

    def send_rc_command(self, channels):
        """Sends RC commands to the flight controller."""
        if len(channels) != 8:
            raise ValueError("RC command must contain 8 values.")
        self.board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_RAW_RC'], struct.pack('<8H', *channels))


fc = FlightController()

while True:
    try:
        raw_imu_data = fc.read_imu()  # ✅ Read IMU directly here
        scaled_data = scale_imu_data(raw_imu_data)
        orientation = determine_orientation(scaled_data)

        print("IMU Data:", scaled_data)
        print("Orientation:", ", ".join(orientation))

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(0.1)
