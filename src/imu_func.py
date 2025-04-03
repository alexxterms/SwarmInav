import math

def scale_imu_data(raw_data):
    """Scales raw IMU data to meaningful values."""
    raw_accel = raw_data['accelerometer']
    raw_gyro = raw_data['gyroscope']
    raw_mag = raw_data['magnetometer']

    # Convert raw accelerometer data to G-force
    acc_x, acc_y, acc_z = [val / 512.0 for val in raw_accel]

    # Convert raw gyroscope data to degrees per second
    gyro_x = raw_gyro[0] * (4.0 / 16.4)
    gyro_y = raw_gyro[1] * (4.0 / 16.4)
    gyro_z = raw_gyro[2] * (4.0 / 16.4)

    return {
        "accelerometer": [acc_x, acc_y, acc_z],
        "gyroscope": [gyro_x, gyro_y, gyro_z],
        "magnetometer": raw_mag
    }

def determine_orientation(scaled_data):
    """Determines the flight orientation based on IMU readings."""
    acc_x, acc_y, acc_z = scaled_data["accelerometer"]
    gyro_z = scaled_data["gyroscope"][2]  # Only need z-axis for yaw/turning

    roll_angle = math.degrees(math.atan2(acc_y, acc_z))
    pitch_angle = math.degrees(math.atan2(acc_x, math.sqrt(acc_y**2 + acc_z**2)))

    orientation = []

    if pitch_angle > 10:
        orientation.append("Nose Up")
    elif pitch_angle < -10:
        orientation.append("Nose Down")

    if roll_angle > 10:
        orientation.append("Right Wing Down")
    elif roll_angle < -10:
        orientation.append("Left Wing Down")

    if gyro_z < -5:
        orientation.append("Turning Right")
    elif gyro_z > 5:
        orientation.append("Turning Left")

    if acc_z > 1.1:
        orientation.append("Climbing")
    elif acc_z < 0.9:
        orientation.append("Descending")

    if not orientation:
        orientation.append("Level Flight")

    return orientation

