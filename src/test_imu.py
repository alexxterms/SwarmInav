from yamspy import MSPy

serial_port = "/dev/ttyACM0"

with MSPy(device=serial_port, loglevel='DEBUG', baudrate=115200) as board:
    if board.send_RAW_msg(MSPy.MSPCodes['MSP_ATTITUDE'], data=[]):
        dataHandler = board.receive_msg()
        board.process_recv_data(dataHandler)

        print("📡 Attitude Response:", dataHandler)
