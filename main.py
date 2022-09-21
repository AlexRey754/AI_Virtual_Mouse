import cv2
import numpy as np
import HandTrackModule as htm
import time
import autopy

##########################
wCam, hCam = 640, 480
frameR = 60 # Frame Reduction
smoothening = 8
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()


while True:
    # Поиск точек /
    # find points
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # Получение среднего и указательного пальцев / 
    # middle and forefinger
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)
    
    # Проверка полнятых пальцев
    # Check fingers up
        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)

    # Режим перемещения
    # Move mode
        if fingers[1] == 1 and fingers[2] == 0:
            # Преобразование координат
            # Coordinate transformation
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # Плавное перемещение
            # Smoth moving
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
    
        # Передвижение мыши
        # Moving mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        
    # ЛКМ
    # Left mouse Button
        if fingers[1] == 1 and fingers[2] == 1:

            # Рвастояние между пальцами
            # Distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img,draw=False)

            # Нажать если дистанция очень маленькая
            # Press if the distance is too small
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

    # Отображение
    # Display
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == 27:
        break