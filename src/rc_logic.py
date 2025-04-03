import time

def update_rc_data(shared_rc_data):
    """Continuously updates the RC data."""
    try:
        while True:
            # Example logic to modify RC data (this should be customized)
            shared_rc_data[0] = 1500  # Roll
            shared_rc_data[1] = 1500  # Pitch
            shared_rc_data[2] = 1500  # Throttle
            shared_rc_data[3] = 1500  # Yaw
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("⏹️ Stopping RC updates.")
