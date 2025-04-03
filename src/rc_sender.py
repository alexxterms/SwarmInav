import time
import threading
from yamspy import MSPy
from multiprocessing import Array
from rc_logic import update_rc_data
import imu_reader

def send_rc_commands(board, shared_rc_data):
    try:
        while True:
            # Read the latest RC data from the shared Array
            rc_data = list(shared_rc_data)
            print(f"Sending RC data: {rc_data}")  # Debug print to see values being sent
            board.send_RAW_RC(rc_data)  # Send the RC data
            time.sleep(0.1)  # Maintain 10Hz refresh rate (100 ms)
    except KeyboardInterrupt:
        print("Stopping RC updates.")
    finally:
        board.disconnect()    
        

if __name__ == "__main__":
    # Initialize the MSPy board connection
    board = MSPy('/dev/ttyUSB5', 115200)
    board.connect()
    imu_data = imu_reader.read_imu(board)
    # Shared RC data
    shared_rc_data = Array('i', [1500, 1500, 1000, 1000, 1000, 1000, 1000, 1000])
    if imu_data:
        acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = imu_data
        print(f"IMU Data - Acc: ({acc_x}, {acc_y}, {acc_z}) | Gyro: ({gyro_x}, {gyro_y}, {gyro_z})")
    # Start the RC data update logic in a separate thread
    rc_update_thread = threading.Thread(target=update_rc_data, args=(shared_rc_data,))
    rc_update_thread.daemon = True  # Allows the program to exit when main thread exits
    rc_update_thread.start()

    # Start sending RC commands
    send_rc_commands(board, shared_rc_data)

