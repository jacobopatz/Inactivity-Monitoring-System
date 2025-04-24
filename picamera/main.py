import time
from datetime import datetime, timezone
import sys
from camera import capture_frame, test_capture
from detector import detect_person
import requests

INTERVAL_SECONDS = 1
BACKEND_URL = "http://127.0.0.1:5000/upload"

in_bed = False
start_time = None
# Test function to send a piece of test data to the backend
def send_test_data():
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "person_detected": False, # Example value
    }
    try:
        response = requests.post(BACKEND_URL, json=payload)
        print(f"Test data sent: {response.json()}")
    except Exception as e:
        print(f"Error sending test data to backend: {e}")

# Call the test function


def send_to_backend(person_detected):
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "person_detected": person_detected
    }
    try:
        response = requests.post(BACKEND_URL, json=payload)
        print(f"Data sent: {response.json()}")
    except Exception as e:
        print(f"Error sending data to backend: {e}")


def main():
    global in_bed
    while True:
        try:
            # frame = capture_frame()
            frame = capture_frame()
            personFound = detect_person(frame)
            # send_detection(person_found, BACKEND_URL)
            if personFound != in_bed:
                print("Person is in bed!")
                
                if personFound:
                    print("Person detected!")
                else:
                    print("Person not detected!")
                
                send_to_backend(personFound)
            else:
                print("No change in detection status.")
                
        except Exception as e:
            print(f"Error in loop: {e}")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        send_test_data()
    else:
        main()