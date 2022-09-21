import cv2 as cv
import mediapipe as mp
import time

class handDetector:
    def __init__(self,mode=False,maxHands=2,detectionConf=0.5,trackConf=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionConf=detectionConf
        self.trackConf=trackConf
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxHands,self.detectionConf,self.trackConf)
        self.mpDraw=mp.solutions.drawing_utils

    def findHands(self,frame,draw=True):
        imgRGB=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLMs in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame,handLMs,self.mpHands.HAND_CONNECTIONS)
        return frame

    def findPos(self,frame,handNum=0,draw=True):
        LMlist=[]
        if self.results.multi_hand_landmarks: 
            myHand=self.results.multi_hand_landmarks[handNum]
            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h,w,ch=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                # print(id,cx,cy)
                LMlist.append([id,cx,cy])
                if draw:
                    cv.circle(frame,(cx,cy),5,(0,255,0),cv.RNG_UNIFORM)
            return LMlist

def main():
    pTime=0
    cTime=0
    capture=cv.VideoCapture(0,cv.CAP_DSHOW)
    detector=handDetector()
    while True:
        isTrue, frame=capture.read()
        frame=detector.findHands(frame)
        lmlist=detector.findPos(frame)
        if len(lmlist)!=0 :
            print(lmlist[8])
        else:
            print('Not found')
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv.putText(frame,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(0,0,255),2)
        cv.imshow('video',frame)
        if cv.waitKey(20) & 0xFF==ord('q'):
            break
    capture.release()
    cv.destroyAllWindows()

if __name__=="__main__":
    main()