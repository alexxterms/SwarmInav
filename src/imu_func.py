import math

def get_imu_data(fc):

    return fc.read_imu()

def scale_imu_data(imu_data):
    """Scales accelerometer, gyroscope, and magnetometer values for better readability."""
    scaled_data = {
        "accelerometer": [val for val in imu_data["accelerometer"]],
        "gyroscope": [val for val in imu_data["gyroscope"]],
        "magnetometer": [val for val in imu_data["magnetometer"]],
    }
    return scaled_data

def determine_orientation(imu_data):
    """Determines the drone's orientation using accelerometer and gyroscope data."""
    accel = imu_data["accelerometer"]
    gyro = imu_data["gyroscope"]
    
    roll_angle = math.degrees(math.atan2(accel[1], accel[2]))
    pitch_angle = math.degrees(math.atan2(-accel[0], math.sqrt(accel[1]**2 + accel[2]**2)))

    orientation = []

    if pitch_angle > 10:
        orientation.append("Nose Up")
    elif pitch_angle < -10:
        orientation.append("Nose Down")

    if roll_angle > 10:
        orientation.append("Right Wing Down")
    elif roll_angle < -10:
        orientation.append("Left Wing Down")

    if gyro[2] > 5:
        orientation.append("Turning Right")
    elif gyro[2] < -5:
        orientation.append("Turning Left")

    if accel[2] > 1.1:
        orientation.append("Climbing")
    elif accel[2] < 0.9:
        orientation.append("Descending")

    if not orientation:
        orientation.append("Level Flight")

    return orientation
