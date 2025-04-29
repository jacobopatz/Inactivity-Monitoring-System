import time
from datetime import datetime
import sys
import requests
from camera import capture_frame, test_capture
from detector import detect_person

INTERVAL_SECONDS = 20
BACKEND_URL = "http://127.0.0.1:5000/upload"

in_bed = False
start_time = None

# Test function to send a piece of test data to the backend
def send_test_data():
    payload = {
        "timestamp": datetime.now().isoformat(),
        "duration": 5.0  # Example duration
    }
    try:
        response = requests.post(BACKEND_URL, json=payload)
        print(f"Test data sent: {response.json()}")
    except Exception as e:
        print(f"Error sending test data to backend: {e}")

# Function to send actual data to the backend
def send_to_backend(start_time, duration_seconds,person_detected):
    duration_minutes = int(duration_seconds) / 60
    payload = {
        "start_time":start_time.isoformat(),
        "duration_minutes": duration_minutes,
        "person_detected": person_detected
    }
    try:
        response = requests.post(BACKEND_URL, json=payload)
        print(f"Data sent: {response.json()}")
    except Exception as e:
        print(f"Error sending data to backend: {e}")

def main():
    global in_bed, start_time
    start_time = datetime.now()
    while True:
        try:
           
            frame = capture_frame()
            person_found = detect_person(frame)

            if person_found: 
                if not in_bed:
                    print("Person is in bed!")
                    duration = (datetime.now() - start_time).total_seconds()
                    in_bed = True
                    start_time = datetime.now()
                else:
                    print("person still in bed")

            else:
                if not in_bed:
                    print("no person detected")

                else:
                    print("Person left bed")
                    duration = (datetime.now() - start_time).total_seconds()
                    send_to_backend(start_time,duration, in_bed)
                    start_time = datetime.now()
                    in_bed = False
                    print(f"Sent Duration: {duration} seconds to backend")
                    
        except:
            print("Error sending to back end")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        send_test_data()
    else:
        main()
