from main import send_to_backend
from datetime import datetime, timedelta
import random
import sys
def main():
    delta = int(input("Enter hours from now (+/-) your session started: "))
    duration = int(input("enter number of minutes your session lasted: "))
    in_bed = bool(input('(True/False)- a person was in bed for this session: '))
    duration = duration * 60
    send_to_backend((datetime.now() + timedelta(hours = delta)),duration,in_bed )

def populate_test_data():
    times = [30,45,105,40,60,80]
    weeks_to_fill = 5
    days = weeks_to_fill * 7
    inc = 0
    now = datetime.now()
    start_date = now - timedelta(days = days)

    while(days >= 0):
        index = random.randint(0,(len(times) - 1))
        duration = times[index] * 60
        send_to_backend(start_date,duration,True)
        start_date = start_date + timedelta(days=1)
        days -= 1
        inc += 1
        print(f"send{inc} days to backend ")
    print(f'populated {weeks_to_fill} weeks with times')


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        populate_test_data()
    else:
        main()