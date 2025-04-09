import time
import struct
from yamspy import MSPy

port = "/dev/ttyACM1"
baudrate = 115200

with MSPy(device=port, baudrate=baudrate) as board:
    if board.connect(trials=3):
        print("✅ Connected")
    else:
        raise Exception("❌ Could not connect")

    while True:
        if board.send_RAW_msg(MSPy.MSPCodes['MSP_STATUS']):
            dataHandler = board.receive_msg()
            if dataHandler:
                payload = dataHandler.get('dataView', bytearray())
                if len(payload) >= 10:
                    _, _, _, flag, _ = struct.unpack('<5H', payload[:10])
                    armed = bool(flag & (1 << 0))
                    print("🚁 Drone is", "✅ ARMED" if armed else "❌ DISARMED")
                else:
                    print("⚠️ Incomplete payload")
            else:
                print("⚠️ No data received")
        else:
            print("⚠️ Failed to send MSP_STATUS")

        time.sleep(1)
