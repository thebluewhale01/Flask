import cv2

cap = cv2.VideoCapture(0)
while True:
    _, image = cap.read()

    cv2.imshow("Video", image)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()