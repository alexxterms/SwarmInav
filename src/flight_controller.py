import time
import struct
from yamspy import MSPy
from imu_func import scale_imu_data, determine_orientation  # ✅ Import from imu_func.py

# UART Configuration
imu_port = "/dev/ttyUSB0"  # IMU on UART0
rc_port = "/dev/ttyUSB1"   # RC control on UART1
baudrate = 115200

# Throw Detection Threshold
throw_threshold = 15  # Adjust the threshold to detect sudden spikes in acceleration

# Flag for throw detection
throw_detected = False

# Open connections using "with" to ensure proper handling
with MSPy(device=imu_port, baudrate=baudrate) as imu_board, MSPy(device=rc_port, baudrate=baudrate) as rc_board:
    if imu_board.connect(trials=3) and rc_board.connect(trials=3):
        print("✅ Both UARTs connected successfully")
    else:
        raise Exception("❌ Failed to connect to one or both serial ports")

    imu_interval = 0.02   # 50Hz (every 20 ms)
    rc_interval = 0.05    # 20Hz (every 50 ms)

    last_imu_time = time.time()
    last_rc_time = time.time()

    while True:
        current_time = time.time()

        # Read IMU data
        if current_time - last_imu_time >= imu_interval:
            if imu_board.send_RAW_msg(MSPy.MSPCodes['MSP_RAW_IMU']):
                dataHandler = imu_board.receive_msg()
                imu_board.process_recv_data(dataHandler)

                raw_imu = {
                    "accelerometer": imu_board.SENSOR_DATA["accelerometer"],
                    "gyroscope": imu_board.SENSOR_DATA["gyroscope"],
                    "magnetometer": imu_board.SENSOR_DATA["magnetometer"]
                }

                scaled_imu = scale_imu_data(raw_imu)  # ✅ Use function from imu_func.py
                orientation = determine_orientation(scaled_imu)  # ✅ Use function from imu_func.py

                print("IMU:", scaled_imu)
                print("Orientation:", ", ".join(orientation))

                # Check for Throw Trigger (detecting sudden acceleration spike)
                acceleration_z = scaled_imu["accelerometer"][2]  # Z-axis acceleration (vertical)
                if acceleration_z > throw_threshold and not throw_detected:
                    throw_detected = True
                    print("✅ Throw Detected! Switching to Autonomous Mode")
                    # You can set any necessary modes here for autonomous flight, like:
                    # - Enable stabilization, altitude hold, GPS mode, etc.
                    # For example, you might set RC channels to autonomous commands here
                    # or send a signal to the flight controller to start autonomous mode.

            last_imu_time = current_time

        # Send RC command if not in throw mode (manual control mode)
        if not throw_detected:
            if current_time - last_rc_time >= rc_interval:
                rc_values = [1500] * 8  # Neutral values for manual control
                rc_board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_RAW_RC'], struct.pack('<8H', *rc_values))
                print("RC sent")
                last_rc_time = current_time

        # Once throw is detected, you could switch to autonomous flight (no RC control).
        if throw_detected:
            # Implement Autonomous Control Logic (e.g., switching modes, sending auto commands)
            # Send autonomous commands or make further adjustments for flight
            print("Autonomous flight active")
            # Example: you might replace RC with preset values for auto mode

        time.sleep(0.01)  # 10ms delay for polling
