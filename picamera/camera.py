import cv2

def capture_frame(camera_index=0):
    #initialize camera and capture frame
    cap = cv2.VideoCapture(camera_index)
    ret, frame = cap.read()

    #write to image (FOR TESTING ONLY)
    cv2.imwrite("captured_frame.jpg", frame)
    cap.release()

    if not ret:
        raise RuntimeError("Failed to capture image from camera.")
    return frame

    #use to load imaged not from the camera, for testing
def test_capture(imageName="captured_frame.jpg"):
    # Load the image from file
    frame = cv2.imread(imageName)
    return frame
     
if __name__ == "__main__":
    capture_frame()