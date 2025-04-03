def scale_imu_data(imu_data):
    """Scales raw IMU data to meaningful values."""
    acc_x, acc_y, acc_z = [val / 512.0 for val in imu_data["accelerometer"]]
    gyro_x, gyro_y, gyro_z = [val * (4.0 / 16.4) for val in imu_data["gyroscope"]]
    mag_x, mag_y, mag_z = imu_data["magnetometer"]

    return {
        "accelerometer": [acc_x, acc_y, acc_z],
        "gyroscope": [gyro_x, gyro_y, gyro_z],
        "magnetometer": [mag_x, mag_y, mag_z]
    }

def determine_orientation(scaled_data):
    """Determines orientation based on gyroscope data."""
    gyro_x, gyro_y, gyro_z = scaled_data["gyroscope"]
    
    roll = "Rolling Left" if gyro_x < -0.1 else "Rolling Right" if gyro_x > 0.1 else "Stable"
    pitch = "Pitching Down" if gyro_y < -0.1 else "Pitching Up" if gyro_y > 0.1 else "Stable"
    yaw = "Yawing Left" if gyro_z < -0.1 else "Yawing Right" if gyro_z > 0.1 else "Stable"

    return [roll, pitch, yaw]
