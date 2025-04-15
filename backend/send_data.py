import requests
import json
from datetime import datetime
import time

SERVER_URL = "http://127.0.0.1:5000"  # Replace with Flask server IP

def send_data(duration):
    """Send bed tracking data to the backend server."""
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "duration": duration
    }
    response = requests.post(SERVER_URL, json=payload)
    print(response.json())

# Simulate tracking (Replace this with actual camera/sensor logic)
while True:
    duration = 7.5  # Replace with actual computed bed time
    send_data(duration)
    time.sleep(10)  # Send data every 10 seconds
