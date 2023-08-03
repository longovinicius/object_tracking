import cv2
#from tracker import *
from tracker import EuclideanDistTracker

video_path = '/home/vini/Documents/Projects/Tracking/object_tracking/highway.mp4'

# Captures video file
cap = cv2.VideoCapture(video_path)

tracker = EuclideanDistTracker()

# Check if the video capture object is created successfully
if not cap.isOpened():
    print("Error: Video capture object not created successfully.")
else:
    print("Video capture object created successfully.")


# Detect moving elements
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

while True:
    ret, frame = cap.read()

    roi = frame[340:720, 500:800]

    # 1.Object Detection
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detections = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:
            cv2.drawContours(roi, [contour], -1, (0,255,0))
            x, y, h, w = cv2.boundingRect(contour)
            detections.append([x, y, h, w])

    # 2.Object Tracktion
    objects_bbs_ids = tracker.update(detections)
    print(objects_bbs_ids)

    cv2.imshow("Frame", frame)
    #cv2.imshow("Mask", mask)

    key = cv2.waitKey(30)
    if key == 27: # esc buttom
        break 

cap.release()
cv2.destroyAllWindows()
