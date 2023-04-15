import cv2
import mediapipe as mp
import time  # for frame rate
import pyautogui as pgui

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()  # only takes img in RGB form
mpDraw = mp.solutions.drawing_utils
x1=y1=x2=y2=0

cTime = 0  # current time
pTime = 0  # previous time

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    res=results.multi_hand_landmarks
    frame_width , frame_height ,_ = img.shape

    if res:
        for hand in res:
            #mpDraw.draw_landmarks(img, hand)         handconnections(a parameter in draw_landmarks)=lines btwn lndmrk pts
            mpDraw.draw_landmarks(img, hand)
            landmarks= hand.landmark
            #if landmarks:
            for id,landmark in enumerate(landmarks):
                x = int(landmark.x * frame_height)
                y = int(landmark.y * frame_width)
                if id == 4:
                    cv2.circle(img,(x,y),8,(0,255,255),-1)
                    x1=x
                    y1=y

                if id == 8:
                    cv2.circle(img,(x,y),8,(0,255,0),-1)
                    x2=x
                    y2=y

            dist=((x2-x1)**2+(y2-y1)**2)**0.5//4
            print(dist)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),4)

        if dist > 50:
            pgui.press("volumeup")
        else:
            pgui.press("volumedown")


    cTime = time.time()
    fps = 1 / (cTime - pTime)  # frame rate per second
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)


    cv2.imshow("image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
