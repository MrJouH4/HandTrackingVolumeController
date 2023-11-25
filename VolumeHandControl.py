import cv2
import time
import mediapipe as mp
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

#####################################
wCam, hCam = 640, 480
#####################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.9)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()
minVol = volumeRange[0]
maxVol = volumeRange[1]
print(volumeRange)


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255,0,255), 3)
        cv2.circle(img, (cx, cy), 10, (255,0,255), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)
        print("Length: ", length)
        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0,255,0), cv2.FILLED)
        vol = np.interp(length, [50,200], [minVol, maxVol])
        print("Volume: ", vol)
        volume.SetMasterVolumeLevel(vol, None)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f"FPS: {int(fps)}", (10,30), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)