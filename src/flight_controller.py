import time
import struct
import threading
from yamspy import MSPy
from imu_func import scale_imu_data, determine_orientation  

# UART Configuration
imu_port = "/dev/ttyACM0"  # IMU through FC USB C
rc_port = "/dev/ttyUSB0"   # RC control through FC Uart
baudrate = 115200

# Throw Detection Parameters
throw_threshold = 15  # Threshold for accel (throw func) In Gs on Z axis
altitude_threshold = 2  # Threshold for altitude (throw func) in meters

# Flags and variables
throw_detected = False
previous_altitude = 0
apogee_reached = False
arm_check = False

# Shared RC command array
rc_values = [1500] * 8
rc_lock = threading.Lock()

# Thread to check arming status every 2 seconds
def arm_status_checker():
    global arm_check
    while True:
        if imu_board.send_RAW_msg(MSPy.MSPCodes['MSP_STATUS']):
            dataHandler = imu_board.receive_msg()
            imu_board.process_recv_data(dataHandler)

            flags = imu_board.SENSOR_DATA.get("flag")
            if flags is not None:
                armed = bool(flags & 0b00000001)
                arm_check = armed
                print("🔍 Drone Armed" if armed else "🔍 Drone Disarmed")
            else:
                print("⚠️ Could not find 'flag' in status")
        time.sleep(2)


# RC logic func that will be run in a different thread
def rc_logic():
    global throw_detected, arm_check, rc_values
    while True:
        with rc_lock:
            #Our throw rc logic
            if throw_detected:
                if not arm_check:
                    rc_values[2] = 885     # Throttle Low before arming(CH3)
                    rc_values[4] = 2000    # Arm (CH5)
                    rc_values[5] = 1000    # Position Hold low  (CH6)
                    rc_values[6] = 1000    # Angle Mode on CH7 always on
                    arm_check = True
                    print("✅ First arm command set")
                    time.sleep(0.1)  # Small delay before increasing throttle
                else:
                    rc_values[2] = 1300     # Increase Throttle after arming
                    rc_values[5] = 2000    # Position Hold ON (CH6)
                    print("🚀 Autonomous RC command updated")
            else:
                rc_values = [1500] * 8  # Neutral values for manual mode
                rc_values[6] = 1000  # Angle mode alwayss
        time.sleep(0.05)  # 20Hz

# This will be one big heck of a non modular code but anyways
# Open connections using "with" kill me
with MSPy(device=imu_port, baudrate=baudrate) as imu_board, MSPy(device=rc_port, baudrate=baudrate) as rc_board:
    if imu_board.connect(trials=3) and rc_board.connect(trials=3): #will try 3 times to connect
        print("✅ Both UARTs connected successfully")
    else:
        raise Exception("❌ Failed to connect to one or both serial ports")

    # Start RC logic in a separate thread
    rc_thread = threading.Thread(target=rc_logic, daemon=True)
    rc_thread.start()

    # Start arming status checker thread
    arm_status_thread = threading.Thread(target=arm_status_checker, daemon=True)
    arm_status_thread.start()


    imu_interval = 0.02   # 50Hz (every 20 ms)
    alt_interval = 0.1    # 10Hz (every 100 ms)
    rc_interval = 0.1     # 10Hz (every 100 ms)   VERY IMP 

    last_imu_time = time.time()
    last_alt_time = time.time()
    last_rc_time = time.time()

    while True:
        current_time = time.time()

        ########################################  Read IMU data  ######################################################
        if current_time - last_imu_time >= imu_interval:
            if imu_board.send_RAW_msg(MSPy.MSPCodes['MSP_RAW_IMU']):
                dataHandler = imu_board.receive_msg()
                imu_board.process_recv_data(dataHandler)

                raw_imu = {
                    "accelerometer": imu_board.SENSOR_DATA["accelerometer"],
                    "gyroscope": imu_board.SENSOR_DATA["gyroscope"],
                    "magnetometer": imu_board.SENSOR_DATA["magnetometer"]
                }

                scaled_imu = scale_imu_data(raw_imu)  
                orientation = determine_orientation(scaled_imu)  

                print("IMU:", scaled_imu)
                print("Orientation:", ", ".join(orientation))

                # Check for Throw Trigger (detecting sudden acceleration spike)
                acceleration_z = scaled_imu["accelerometer"][2]  # Z-axis acceleration (vertical)
                if acceleration_z > throw_threshold and not throw_detected:
                    print("✅ Possible Throw Detected! Waiting for Altitude Confirmation...")

            last_imu_time = current_time

        ########################################  Read Altitude Data  #################################################3
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

        ######################################  Send RC commands at 10Hz  ###################################################
        if current_time - last_rc_time >= rc_interval:
            with rc_lock:
                rc_board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_RAW_RC'], struct.pack('<8H', *rc_values))
                print("RC command sent")
            last_rc_time = current_time

        time.sleep(0.01)  # 10ms delay for polling
# Too many print statements i know, will remove it after proper testing