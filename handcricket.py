import random
import cv2
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
initialTime = time.time()
stateResult = False
startGame = True
stop= False
scores = [0, 0] 
computer_image=cv2.resize(cv2.imread("Resources\Resources\{}.png".format(0)),(0,0),None,1.5,1.5)
while True:
    imgBG = cv2.imread("Resources/Resources/Background.png")
    success, img = cap.read()
    if success:
        imgScaled = cv2.resize(img, (0, 0), None, 0.625, 0.625)
        imgScaled = imgScaled[:, 100:400]
    else:
        continue
    
    hands, img = detector.findHands(imgScaled)

    if startGame:

        if stateResult is False:
            
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(3-int(timer)), (610, 420), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True

                if hands:
                    playerMove = 0
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 0
                    elif fingers == [0, 0, 0, 0, 1] or fingers == [0, 1, 0, 0, 0]:
                        playerMove = 1
                    elif fingers == [0, 0, 0, 1, 1] or fingers == [0, 1, 1, 0, 0]:
                        playerMove = 2
                    elif fingers == [0, 0, 1, 1, 1] or fingers == [0, 1, 1, 1, 0]:
                        playerMove = 3
                    elif fingers == [0, 1, 1, 1, 1]:
                        playerMove = 4
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 5
                    elif fingers == [1, 0, 0, 0, 0]:
                        playerMove = 6
                    else:
                        playerMove="-"

                    randomNumber = random.randint(1, 6)
                    computer_image=cv2.resize(cv2.imread("Resources\Resources\{}.png".format(randomNumber)),(0,0),None,300/234,300/234)
                    scores[0] = randomNumber
                    if randomNumber==playerMove:
                        stop=True
                    elif playerMove != "-":
                        scores[1] += playerMove
                    
    imgBG[248:548,120:420]=computer_image
    imgBG[232:532, 844:1144] = imgScaled

    cv2.putText(imgBG, str(scores[0]), (250, 235), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (990, 225), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.imshow("Hand Cricket", imgBG)

    key = cv2.waitKey(1)
    if timer>3:  
        initialTime = time.time()
        timer=0
        stateResult=False
    if stop:
        cv2.putText(imgBG,"Press S to Start a new game!", (135, 386), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 223, 225), 6)
        cv2.imshow("Hand Cricket",imgBG)
        k=cv2.waitKey(1)
        while k!=ord('s'):
            k=cv2.waitKey(1)
        stop=False
        scores=[0,0]
    if key== ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
        