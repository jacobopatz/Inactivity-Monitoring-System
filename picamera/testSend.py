from main import send_to_backend
from datetime import datetime, timedelta
def main():
    delta = int(input("Enter hours from now (+/-) your session started: "))
    duration = int(input("enter number of minutes your session lasted: "))
    in_bed = bool(input('(True/False)- a person was in bed for this session: '))
    duration = duration * 60
    send_to_backend((datetime.now() + timedelta(hours = delta)),duration,in_bed )

if __name__ == "__main__":
    
    main()