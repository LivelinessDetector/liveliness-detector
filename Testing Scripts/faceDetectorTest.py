import cvzone
from cvzone.FaceDetectionModule import FaceDetector
import cv2

# Initialize the webcam
cap = cv2.VideoCapture(1)  # Try changing the index if needed

# Initialize the FaceDetector object
detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)

# Run the loop to continually get frames from the webcam
while True:
    # Read the current frame from the webcam
    success, img = cap.read()

    # Check if the frame was captured successfully
    if not success:
        print("Failed to capture image from camera.")
        break

    # Detect faces in the image
    img, bboxs = detector.findFaces(img, draw=False)

    # Check if any face is detected
    if bboxs:
        for bbox in bboxs:
            center = bbox["center"]
            x, y, w, h = bbox['bbox']
            score = int(bbox['score'][0] * 100)

            # Draw data on the image
            cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
            cvzone.putTextRect(img, f'{score}%', (x, y - 10))
            cvzone.cornerRect(img, (x, y, w, h))

    # Display the image
    cv2.imshow("Image", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()