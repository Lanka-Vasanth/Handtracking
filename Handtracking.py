import cv2 as cv
import mediapipe as mp
import time

capture=cv.VideoCapture(0)

mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
pTime=0
cTime=0

while True:
    isTrue, frame=capture.read()
    imgRGB=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLMs in results.multi_hand_landmarks:
            for id, lm in enumerate(handLMs.landmark):
                # print(id,lm)
                h,w,ch=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                print(id,cx,cy)
                if id==0:
                    cv.circle(frame,(cx,cy),10,(0,255,0),cv.FILLED)
            mpDraw.draw_landmarks(frame,handLMs,mpHands.HAND_CONNECTIONS)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv.putText(frame,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(0,0,255),2)
    cv.imshow('video',frame)
    if cv.waitKey(20) & 0xFF==ord('q'):
        break

capture.release()
cv.destroyAllWindows()