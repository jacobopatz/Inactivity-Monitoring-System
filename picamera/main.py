import time
import sys
from camera import capture_frame, test_capture
from detector import detect_person

INTERVAL_SECONDS = 1

def main():
    while True:
        try:
            # frame = capture_frame()
            frame = capture_frame()
            personFound = detect_person(frame)
            # send_detection(person_found, BACKEND_URL)
            if(personFound):
                print("person detected!!")
            else:
                print("no person detected")
        except Exception as e:
            print(f"Error in loop: {e}")
        time.sleep(INTERVAL_SECONDS)
def test():
    while True:
        try:
            # frame = capture_frame()
            frame = test_capture()
            personFound = detect_person(frame)
            # send_detection(person_found, BACKEND_URL)
            if(personFound):
                print("person detected!!")
            else:
                print("no person detected")
        except Exception as e:
            print(f"Error in loop: {e}")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        main()