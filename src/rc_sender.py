import time
import threading
from multiprocessing import Array
from flight_controller import FlightController
from rc_logic import update_rc_data
from imu_reader import read_imu_continuous

def send_rc_commands(fc, shared_rc_data):
    """Continuously sends RC commands to the flight controller."""
    try:
        while True:
            rc_data = list(shared_rc_data)
            print(f"🚀 Sending RC data: {rc_data}")
            fc.send_rc_commands(rc_data)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("⏹️ Stopping RC updates.")
    finally:
        fc.disconnect()

if __name__ == "__main__":
    # Initialize the flight controller
    fc = FlightController()

    # Shared memory for RC commands
    shared_rc_data = Array('i', [1500, 1500, 1000, 1000, 1000, 1000, 1000, 1000])

    # Start the IMU reading thread
    imu_thread = threading.Thread(target=read_imu_continuous, args=(fc,))
    imu_thread.daemon = True
    imu_thread.start()

    # Start the RC update thread
    rc_update_thread = threading.Thread(target=update_rc_data, args=(shared_rc_data,))
    rc_update_thread.daemon = True
    rc_update_thread.start()

    # Start sending RC commands
    send_rc_commands(fc, shared_rc_data)
