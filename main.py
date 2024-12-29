import cv2
import os
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("Resources/Background.png")

# Importando todas as imagens para uma lista
folderPathModes = "Resources/Modes"
listOfImgModesPath = os.listdir(folderPathModes)
listOfImgModes = []
for imgModePath in listOfImgModesPath:
    listOfImgModes.append(cv2.imread(os.path.join(folderPathModes, imgModePath)))
print(listOfImgModes)

# Importando todos os icones para uma lista
folderPathIcons = "Resources/Icons"
listOfImgIconsPath = os.listdir(folderPathIcons)
listOfImgIcons = []
for imgIconsPath in listOfImgIconsPath:
    listOfImgIcons.append(cv2.imread(os.path.join(folderPathIcons, imgIconsPath)))
print(listOfImgIcons)

modeType = 0 # Seleciona o mode
selection = -1
counter = 0
selectionSpeed = 7
modePositions = [(1136, 196), (1000, 384), (1136, 581)]
counterPause = 0
selectionList = [-1, -1, -1]
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    # Encontrar a mão e seus pontos de referência
    hands, img = detector.findHands(img)

    # Overlay da webcam e imagens no background
    imgBackground[139:139 + 480, 50:50 + 640] = img
    imgBackground[0:720, 847:1280] = listOfImgModes[modeType]

    if hands and counterPause == 0 and modeType<3:
            # Informação da mão detectada
            hand1 = hands[0]
            # Conta o número de dedos levantados na mão
            fingers1 = detector.fingersUp(hand1)
            print(fingers1)

            if fingers1 == [0,1,0,0,0]:
                if selection != 1:
                     counter = 1
                selection = 1
            elif fingers1 == [0,1,1,0,0]:
                if selection != 2:
                     counter = 1
                selection = 2
            elif fingers1 == [0,1,1,1,0]:
                if selection != 3:
                     counter = 1
                selection = 3
            else:
                 selection = -1
                 counter = 0

            if counter > 0:
                 counter += 1
                 print(counter)

                 cv2.ellipse(imgBackground, modePositions[selection-1], (103, 103), 0, 0,
                              counter*selectionSpeed, (0, 255, 0), 20)
                 if counter*selectionSpeed > 360:
                      selectionList[modeType] = selection
                      modeType += 1
                      counter = 0
                      selection = -1
                      counterPause = 1

    # Pausa depois de cada seleção
    if counterPause > 0:
         counterPause += 1
         if counterPause > 40:
              counterPause = 0

    # Adiciona icone de seleção embaixo
    if selectionList[0] != -1:
         imgBackground[636:636 + 65, 133:133 + 65] = listOfImgIcons[selectionList[0]-1]

    if selectionList[1] != -1:
         imgBackground[636:636 + 65, 340:340 + 65] = listOfImgIcons[2+selectionList[1]]

    if selectionList[2] != -1:
         imgBackground[636:636 + 65, 542:542 + 65] = listOfImgIcons[5+selectionList[2]]
    
    # Display
    # cv2.imshow("Image", img)
    cv2.imshow("Background", imgBackground)
    cv2.waitKey(1)