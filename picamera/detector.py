from ultralytics import YOLO
import cv2
# Load the model once
model = YOLO("yolov8n.pt")  # or a custom path

def detect_person(frame):
    results = model(frame)
    results = model(frame)
    get_annotated_output(results)
    detections = results[0].boxes.cls.tolist()  # list of class IDs
    personDetected = (0 in detections)
    print(0 in detections)
    return personDetected

    
#Save an annotated version of the image with model detections 
def get_annotated_output(results):
    for result in results:
        annotated_frame = result.plot()  # draws boxes, labels, and confidence

        # Save the image
        cv2.imwrite("annotated_frame.jpg", annotated_frame)
if __name__ == "__main__":
    
    detect_person(frame)