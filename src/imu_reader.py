"ALL THE FUNCTIONS RELATED TO IMU ARE IN THIS FILE"

from yamspy import MSPy

def read_imu(board):
    """
    Reads IMU data from iNav using MSP_RAW_IMU.
    """
    board.send_RAW_msg(MSPy.MSPCodes['MSP_RAW_IMU'], data=[])

    response = board.receive_msg()
    if response and response.cmd == MSPy.MSPCodes['MSP_RAW_IMU']:
        acc_x, acc_y, acc_z = response.data[:3]  # Extract accelerometer values
        gyro_x, gyro_y, gyro_z = response.data[3:6]  # Extract gyroscope values
        return acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z
    
    return None  # Return None if no data is received
