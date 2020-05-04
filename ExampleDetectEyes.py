import time
import cv2
import mss
import numpy as np

from CameraController import XiaomiYiController


Camera = XiaomiYiController()

Camera.ConnectToServer()

with mss.mss() as ScreenCapturing:

    ScreenObject = {"top": 40, "left": 0, "width": 550, "height": 330}

    cv2.namedWindow("output", cv2.WINDOW_NORMAL)

    Camera.PartOneStartVideoToGetCapture()

    while "Screen capturing":

        last_time = time.time()

        img = np.array(ScreenCapturing.grab(ScreenObject))

        face_csc = cv2.CascadeClassifier('haarcascade_eye.xml')

        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        
        eyes = face_csc.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 4, minSize = (10, 10))

        index = 0

        for (x, y, w, h) in eyes:
            
            cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow("output", gray)

        print("fps: {}".format(1 / (time.time() - last_time)))

        if cv2.waitKey(25) & 0xFF == ord("q"):

            cv2.destroyAllWindows()

            Camera.StopVideo()

            break

