import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import socket

width,height=1280,720

capture=cv.VideoCapture(0)
capture.set(3,width)
capture.set(4,height)

detector=HandDetector(maxHands=1,detectionCon=0.8)

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverAddressPort=("127.0.0.1",6969)

while True:
    isTrue,frame=capture.read()
    hands,frame=detector.findHands(frame)

    data=[]
    if hands:
        hand=hands[0]
        lmlist=hand['lmList']
        # print(lmlist)

    for lm in lmlist:
        data.extend([lm[0],height-lm[1],lm[2]])

    # print(data)
    sock.sendto(str.encode(str(data)),serverAddressPort)
    cv.imshow('video',frame)
    if cv.waitKey(20) & 0xFF==ord('q'):
        break

capture.release()
cv.destroyAllWindows()