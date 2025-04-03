from yamspy import MSPy

class FlightController:
    def __init__(self, port='/dev/ttyACM0', baudrate=115200):
        try:
            self.board = MSPy(port, baudrate)
            self.board.connect()
            print("✅ Connected to flight controller.")
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            self.board = None

    def send_rc_commands(self, rc_data):
        """Send RC commands to the flight controller."""
        if self.board:
            self.board.send_RAW_RC(rc_data)

    def read_imu(self):
        if self.board.send_RAW_msg(MSPy.MSPCodes['MSP_RAW_IMU'], data=[]):
            dataHandler = self.board.receive_msg()
            self.board.process_recv_data(dataHandler)

            # Print raw response for debugging
            print(f"📡 Raw IMU Response: {dataHandler}")

            # Check if SENSOR_DATA has the required IMU values
            if 'accX' in self.board.SENSOR_DATA and 'gyroX' in self.board.SENSOR_DATA:
                print(self.board.SENSOR_DATA['gyroX'])
                return (
                    self.board.SENSOR_DATA['accX'], self.board.SENSOR_DATA['accY'], self.board.SENSOR_DATA['accZ'],
                    self.board.SENSOR_DATA['gyroX'], self.board.SENSOR_DATA['gyroY'], self.board.SENSOR_DATA['gyroZ']
                )
        return None


    def disconnect(self):
        """Disconnect from the flight controller."""
        if self.board:
            self.board.disconnect()
            print("🔌 Disconnected.")

# Example usage:
if __name__ == "__main__":
    fc = FlightController()
    print(fc.read_imu())
    fc.disconnect()
