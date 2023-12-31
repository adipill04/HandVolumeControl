import cv2
import time
import numpy as np
import HandtrackerModule as htm
import math
import osascript

pTime = 0
cTime = 0
vidObj = cv2.VideoCapture(0)
vidObj.set(3,640)
vidObj.set(4,480)
detector = htm.handDetector(detectionCon=0.7)
vol = 0

while True:
    success, img = vidObj.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1,y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        vol = np.interp(length, [50, 300], [0, 100])
        volBar = np.interp(length, [50, 300], [400, 150])

        osascript.osascript(f'set volume output volume {vol}')

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

        cv2.rectangle(img, (50,150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'{int(vol)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 250, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(delay=1)


