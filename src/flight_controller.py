import time
import struct
import threading
from yamspy import MSPy
from imu_func import scale_imu_data, determine_orientation  # ✅ Import from imu_func.py

# UART Configuration
imu_port = "/dev/ttyACM4"  # IMU on UART0
rc_port = "/dev/ttyUSB2"   # RC control on UART1
baudrate = 115200

# Throw Detection Parameters
throw_threshold = 15  # Adjust the threshold to detect sudden spikes in acceleration
altitude_threshold = 500  # Minimum altitude to consider a valid throw (in cm)

# Flags and variables
throw_detected = False
previous_altitude = 0
apogee_reached = False
arm_sent = False

# Shared RC command array
rc_values = [1500] * 8
rc_lock = threading.Lock()

# RC Logic Function to modify shared RC values
def rc_logic():
    global throw_detected, arm_sent, rc_values
    while True:
        with rc_lock:
            if throw_detected:
                if not arm_sent:
                    rc_values[2] = 885     # Throttle (CH3)
                    rc_values[4] = 2000    # Arm (CH5)
                    rc_values[5] = 1000    # Position Hold (CH6)
                    rc_values[6] = 1000    # CH7 always ON
                    arm_sent = True
                    print("✅ First arm command set")
                    time.sleep(0.1)  # Small delay before increasing throttle
                else:
                    rc_values[2] = 1300     # Increase Throttle
                    print("🚀 Autonomous RC command updated")
            else:
                rc_values = [1500] * 8  # Neutral values for manual mode
        time.sleep(0.05)  # 20Hz

# Open connections using "with" to ensure proper handling
with MSPy(device=imu_port, baudrate=baudrate) as imu_board, MSPy(device=rc_port, baudrate=baudrate) as rc_board:
    if imu_board.connect(trials=3) and rc_board.connect(trials=3):
        print("✅ Both UARTs connected successfully")
    else:
        raise Exception("❌ Failed to connect to one or both serial ports")

    # Start RC logic in a separate thread
    rc_thread = threading.Thread(target=rc_logic, daemon=True)
    rc_thread.start()

    imu_interval = 0.02   # 50Hz (every 20 ms)
    alt_interval = 0.1    # 10Hz (every 100 ms)

    last_imu_time = time.time()
    last_alt_time = time.time()

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
                    print("✅ Possible Throw Detected! Waiting for Altitude Confirmation...")

            last_imu_time = current_time

        # Read Altitude Data
        if current_time - last_alt_time >= alt_interval:
            if imu_board.send_RAW_msg(MSPy.MSPCodes['MSP_ALTITUDE']):
                dataHandler = imu_board.receive_msg()
                imu_board.process_recv_data(dataHandler)

                altitude = imu_board.SENSOR_DATA.get("altitude", 0)
                print("Altitude:", altitude, "cm")

                # Detect apogee and confirm throw
                if altitude > altitude_threshold and not throw_detected:
                    if altitude < previous_altitude:
                        apogee_reached = True
                        print("✅ Apogee Reached! Throw Confirmed.")
                        throw_detected = True

                previous_altitude = altitude

            last_alt_time = current_time

        # Send RC commands continuously
        with rc_lock:
            rc_board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_RAW_RC'], struct.pack('<8H', *rc_values))
            print("RC command sent")

        time.sleep(0.01)  # 10ms delay for polling
