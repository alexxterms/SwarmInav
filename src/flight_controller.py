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
        """Read IMU data from the flight controller."""
        if self.board:
            response = self.board.send_RAW_MSG(MSPy.MSPCodes['MSP_RAW_IMU'], data=[])
            if response:
                return response['data']  # Adjust based on your IMU data format
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
