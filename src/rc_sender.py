import time
import threading
from yamspy import MSPy
from multiprocessing import Array
from rc_logic import update_rc_data
import imu_reader

def send_rc_commands(board, shared_rc_data):
    """
    Continuously sends RC commands to the flight controller.
    """
    try:
        while True:
            rc_data = list(shared_rc_data)
            print(f"Sending RC data: {rc_data}")  
            board.send_RAW_RC(rc_data)  
            time.sleep(0.1)  # 10Hz refresh rate
    except KeyboardInterrupt:
        print("Stopping RC updates.")
    finally:
        board.disconnect()

def read_imu_continuous(board):
    """
    Reads IMU data continuously in a loop.
    """
    try:
        while True:
            imu_data = imu_reader.read_imu(board)
            if imu_data:
                acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = imu_data
                print(f"IMU Data - Acc: ({acc_x}, {acc_y}, {acc_z}) | Gyro: ({gyro_x}, {gyro_y}, {gyro_z})")
            time.sleep(0.1)  # Adjust the rate as needed
    except KeyboardInterrupt:
        print("Stopping IMU readings.")

if __name__ == "__main__":
    # Initialize MSPy board connectionFi
    try:
        board = MSPy('/dev/ttyACM0', 115200)
        board.connect()
        print("Connected to flight controller.")
    except Exception as e:
        print(f"Failed to connect to flight controller: {e}")
        exit(1)  # Exit if connection fails

    # Shared RC data array
    shared_rc_data = Array('i', [1500, 1500, 1000, 1000, 1000, 1000, 1000, 1000])

    # Start the RC data update logic in a separate thread
    rc_update_thread = threading.Thread(target=update_rc_data, args=(shared_rc_data,))
    rc_update_thread.daemon = True
    rc_update_thread.start()

    # Start the IMU reading thread
    imu_thread = threading.Thread(target=read_imu_continuous, args=(board,))
    imu_thread.daemon = True
    imu_thread.start()

    # Start sending RC commands
    send_rc_commands(board, shared_rc_data)
