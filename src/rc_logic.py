import time
from multiprocessing import Array

# Initialize shared RC data array
rc_data = Array('i', [1500, 1500, 1000, 1000, 1000, 1000, 1000, 1000])

# Individual RC channel variables
throttle = 1000
yaw = 1500
pitch = 1500
roll = 1500
aux1 = 1000
aux2 = 1000
aux3 = 1000
aux4 = 1000

def update_rc_data(shared_rc_data):
    global throttle, yaw, pitch, roll, aux1, aux2, aux3, aux4

    while True:
        # Example: Perform a sequence of movements
        time.sleep(5)
        print("Arming the drone.")
        aux1 = 2000  # Arm
        shared_rc_data[:] = [roll, pitch, throttle, yaw, aux1, aux2, aux3, aux4]

        time.sleep(3)
        print("Pitching forward slightly.")
        slight_pitch_forward(shared_rc_data)

        time.sleep(3)
        print("Pitching backward slightly.")
        slight_pitch_backward(shared_rc_data)

        time.sleep(3)
        print("Rolling right slightly.")
        slight_roll_right(shared_rc_data)

        time.sleep(3)
        print("Rolling left slightly.")
        slight_roll_left(shared_rc_data)

        time.sleep(3)
        print("Yawing right slightly.")
        slight_yaw_right(shared_rc_data)

        time.sleep(3)
        print("Yawing left slightly.")
        slight_yaw_left(shared_rc_data)
        
        time.sleep(3)
        idle(shared_rc_data)

        time.sleep(2)
        print("Disarming the drone.")
        aux1 = 1000  # Disarm
        shared_rc_data[:] = [roll, pitch, throttle, yaw, aux1, aux2, aux3, aux4]
        break

# Function to enable Position Hold mode
def poshold(shared_rc_data):
    global aux3
    aux3 = 1500  # Set AUX3 to 1500 for Position Hold
    shared_rc_data[:] = [roll, pitch, throttle, yaw, aux1, aux2, aux3, aux4]
    print("Position Hold enabled.")

# Function to enable Altitude Hold mode
def althold(shared_rc_data):
    global aux3
    aux3 = 2000  # Set AUX3 to 2000 for Altitude Hold
    shared_rc_data[:] = [roll, pitch, throttle, yaw, aux1, aux2, aux3, aux4]
    print("Altitude Hold enabled.")

# New movement functions
def slight_pitch_forward(shared_rc_data):
    global pitch, throttle
    throttle = 1500
    pitch = 1623  # Adjust pitch for slight forward movement
    shared_rc_data[:] = [roll, pitch, throttle, yaw, aux1, aux2, aux3, aux4]
    print("Pitch forward applied.")

def slight_pitch_backward(shared_rc_data):
    global pitch
    pitch = 1400  # Adjust pitch for slight backward movement
    shared_rc_data[:] = [roll, pitch, throttle, yaw, aux1, aux2, aux3, aux4]
    print("Pitch backward applied.")

def slight_roll_right(shared_rc_data):
    global roll
    roll = 1616  # Adjust roll for slight right movement
    shared_rc_data[:] = [roll, pitch, throttle, yaw, aux1, aux2, aux3, aux4]
    print("Roll right applied.")

def slight_roll_left(shared_rc_data):
    global roll
    roll = 1400  # Adjust roll for slight left movement
    shared_rc_data[:] = [roll, pitch, throttle, yaw, aux1, aux2, aux3, aux4]
    print("Roll left applied.")

def slight_yaw_right(shared_rc_data):
    global yaw
    yaw = 1600  # Adjust yaw for slight right movement
    shared_rc_data[:] = [roll, pitch, throttle, yaw, aux1, aux2, aux3, aux4]
    print("Yaw right applied.")

def slight_yaw_left(shared_rc_data):
    global yaw
    yaw = 1400  # Adjust yaw for slight left movement
    shared_rc_data[:] = [roll, pitch, throttle, yaw, aux1, aux2, aux3, aux4]
    print("Yaw left applied.")

def idle(shared_rc_data):
    global roll, pitch, yaw
    roll = 1500
    pitch = 1500
    yaw = 1500
    shared_rc_data[:] = [roll, pitch , throttle, yaw, aux1, aux2, aux3, aux4]
    
def idle_roll(shared_rc_data):
    global roll
    roll = 1500
    shared_rc_data[:] = [roll, pitch , throttle, yaw, aux1, aux2, aux3, aux4]
    
def idle_pitch(shared_rc_data):
    global pitch
    pitch = 1500
    shared_rc_data[:] = [roll, pitch , throttle, yaw, aux1, aux2, aux3, aux4]
    
def idle_yaw(shared_rc_data):
    global yaw
    yaw = 1500
    shared_rc_data[:] = [roll, pitch , throttle, yaw, aux1, aux2, aux3, aux4]
            
        
