import time
import struct
import threading
from yamspy import MSPy

# UART Configuration
rc_port = "/dev/ttyUSB4"   # RC control on UART
baudrate = 115200

# Shared RC command array
rc_values = [1500] * 8
rc_lock = threading.Lock()

# RC Logic Function to modify shared RC values
def rc_logic():
    global rc_values
    while True:
        with rc_lock:
            rc_values[2] = 900    # Throttle (CH3)
            rc_values[4] = 2000     # Arm (CH5)
            rc_values[5] = 1000    # Position Hold (CH6)
            rc_values[6] = 2000    # CH7 always ON
        time.sleep(0.05)  # Update shared values at 20Hz (optional tuning)

# Open connection using "with" to ensure proper handling
with MSPy(device=rc_port, baudrate=baudrate) as rc_board:
    if rc_board.connect(trials=3):
        print("✅ UART connected successfully")
    else:
        raise Exception("❌ Failed to connect to serial port")

    # Start RC logic in a separate thread
    rc_thread = threading.Thread(target=rc_logic, daemon=True)
    rc_thread.start()

    rc_interval = 0.1  # 10Hz (every 100 ms)
    next_rc_time = time.time()

    while True:
        current_time = time.time()

        # Maintain 10Hz consistent send rate
        if current_time >= next_rc_time:
            with rc_lock:
                rc_board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_RAW_RC'], struct.pack('<8H', *rc_values))
                print("RC command sent")

            next_rc_time += rc_interval

        time.sleep(0.005)  # Light polling delay
