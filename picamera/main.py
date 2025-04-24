import time
from datetime import datetime
import sys
import requests
from camera import capture_frame, test_capture
from detector import detect_person

INTERVAL_SECONDS = 1
BACKEND_URL = "http://127.0.0.1:5000/upload"

in_bed = False
start_time = None

# Test function to send a piece of test data to the backend
def send_test_data():
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "duration": 5.0  # Example duration
    }
    try:
        response = requests.post(BACKEND_URL, json=payload)
        print(f"Test data sent: {response.json()}")
    except Exception as e:
        print(f"Error sending test data to backend: {e}")

# Function to send actual data to the backend
def send_to_backend(duration):
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "duration": duration
    }
    try:
        response = requests.post(BACKEND_URL, json=payload)
        print(f"Data sent: {response.json()}")
    except Exception as e:
        print(f"Error sending data to backend: {e}")

def main():
    global in_bed, start_time
    while True:
        try:
            frame = capture_frame()
            person_found = detect_person(frame)

            if person_found and not in_bed:
                print("Person is in bed!")
                in_bed = True
                start_time = datetime.utcnow()
            elif not person_found and in_bed:
                print("Person just left the bed!")
                in_bed = False
                duration = (datetime.utcnow() - start_time).total_seconds()
                send_to_backend(duration)
                print(f"Sent Duration: {duration} seconds to backend")
            else:
                print("No person detected")
        except Exception as e:
            print(f"Error in loop: {e}")
        
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        send_test_data()
    else:
        main()
