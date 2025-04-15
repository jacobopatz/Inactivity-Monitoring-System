import requests
from datetime import datetime
import sys

def send_detection(PersonFound):
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "person_detected": personFound
    }
    print(payload)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "true":
        send_detection(True)
    else:
        send_detection(False)