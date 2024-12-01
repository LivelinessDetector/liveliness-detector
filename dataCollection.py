import cvzone
from cvzone.FaceDetectionModule import FaceDetector
import cv2
from time import time

###########################################

classID = 0 # 0 is fake, 1 is real
outputFolderPath = 'Dataset/DataCollect'
confidence = 80
save = True
blurThreshold = 35 # larger is more focused
debug = False

offsetPercentageW = 10
offsetPercentageH = 20
camWidth, camHeight = 640, 480
floatingPoint = 6

###########################################

# Initialize the webcam
cap = cv2.VideoCapture(1)  # Try changing the index if needed
cap.set(3, camWidth)
cap.set(4, camHeight)

# Initialize the FaceDetector object
detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)

# Run the loop to continually get frames from the webcam
while True:
    # Read the current frame from the webcam
    success, img = cap.read()
    imgOut = img.copy()

    # Check if the frame was captured successfully
    if not success:
        print("Failed to capture image from camera.")
        break

    # Detect faces in the image
    img, bboxs = detector.findFaces(img, draw=False)

    listBlur = [] # Contains true false values indicating if the faces are blur or not
    listInfo = [] # Normalized values and the calss name for the label text file

    # Check if any face is detected
    if bboxs:
        for bbox in bboxs:
            center = bbox["center"]

            x, y, w, h = bbox['bbox']

            score = int(bbox['score'][0] * 100)

            if score > confidence:
                # adding offset to displayed rectangle
                offsetW = (offsetPercentageW / 100) * w
                x = int(x - offsetW)
                w = int(w + offsetW * 2)

                offsetH = (offsetPercentageH / 100) * h
                y = int(y - offsetH * 3)
                h = int(h + offsetH * 3.5)

                # To avoid values below 0
                if x < 0: x = 0
                if y < 0: y = 0
                if w < 0: w = 0
                if h < 0: h = 0

                # Finding blurriness
                imgFace = img[y: y+h, x: x+w]
                cv2.imshow("Face", imgFace)
                blurValue = int(cv2.Laplacian(imgFace, cv2.CV_64F).var())
                if blurValue > blurThreshold:
                    listBlur.append(True)
                else:
                    listBlur.append(False)


                # Noramalize Values
                ih, iw, _ = img.shape
                xc, yc = x + w/2, y + h/2
                xcn, ycn = round(xc/iw, floatingPoint), round(yc/ih, floatingPoint)
                wn, hn = round(w/iw, floatingPoint), round(h/ih, floatingPoint)
                # print(xcn, ycn, wn, hn)

                # To avoid values above 1
                if xcn > 1: xcn = 1
                if ycn > 1: ycn = 1
                if wn > 1: wn = 1
                if hn > 1: hn = 1

                listInfo.append(f"{classID} {xcn} {ycn} {wn} {hn}\n")

                # Draw data on the image
                cv2.rectangle(imgOut, (x, y, w, h), (255, 0, 0), 3)
                cvzone.putTextRect(imgOut, f'Score: {score}% Blur: {blurValue}', (x, y - 20), scale=1, thickness=2)

                if debug:
                    cv2.rectangle(img, (x, y, w, h), (255, 0, 0), 3)
                    cvzone.putTextRect(img, f'Score: {score}% Blur: {blurValue}', (x, y - 20), scale=1, thickness=2)


        # To save
        if save:
            if all(listBlur) and listBlur != []:
                # Save Image
                timeNow = time();
                timeNow = str(timeNow).split('.')
                timeNow = timeNow[0] + timeNow[1]
                cv2.imwrite(f"{outputFolderPath}/{timeNow}.jpg", img)
                # Save Label text file
                for info in listInfo:
                    f = open(f"{outputFolderPath}/{timeNow}.txt", 'a')
                    f.write(info)
                    f.close()

    # Display the image
    cv2.imshow("Image", imgOut)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()