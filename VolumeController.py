import cv2 as cv
import time
import numpy as np
import HandtrackingMod as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam,hCam=640,480

capture=cv.VideoCapture(0)
capture.set(3,wCam)
capture.set(4,hCam)
pTime=0
cTime=0

detector=htm.handDetector(detectionConf=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMute()
volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-10.0, None)
minVol=volRange[0]
maxVol=volRange[1]
vol=0
volBar=400
volPer=0
while True:
    isTrue,frame=capture.read()
    frame=detector.findHands(frame)
    lmlist=detector.findPos(frame,draw=False)
    # if len(lmlist)!=0:
    #     print(lmlist[4],lmlist[8])
    # elif lmlist==None:
    #     print('None')

    x1,y1=lmlist[4][1],lmlist[4][2]
    x2,y2=lmlist[8][1],lmlist[8][2]
    cx,cy=(x1+x2)//2,(y1+y2)//2
    cv.circle(frame,(cx,cy),3,(0,255,0),3,cv.FILLED)
    cv.circle(frame,(x1,y1),3,(0,255,0),3,cv.FILLED)
    cv.circle(frame,(x2,y2),3,(0,255,0),3,cv.FILLED)

    cv.line(frame,(x1,y1),(x2,y2),(0,0,255),2)

    length=math.hypot(x2-x1,y2-y1)
    # print(int(length))
    
    vol=np.interp(length,[25,200],[minVol,maxVol])
    volBar=np.interp(length,[25,200],[400,150])
    volPer=np.interp(length,[50,300],[0,100])
    print(vol)
    volume.SetMasterVolumeLevel(vol, None)    

    if length<40:
        cv.circle(frame,(cx,cy),3,(255,0,0),3,cv.FILLED)

    cv.rectangle(frame,(50,150),(85,400),(0,255,0),3)
    cv.rectangle(frame,(50,int(volBar)),(85,400),(0,255,0),3)
    cv.putText(frame,str(int(volPer))+'%',(40,450),cv.FONT_HERSHEY_PLAIN,1,(0,255,0),2)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv.putText(frame,str(int(fps)),(30,50),cv.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
    cv.imshow('Video',frame)
    if cv.waitKey(20) & 0xFF==ord('q'):
        break

capture.release()
cv.destroyAllWindows()
