import ai2thor.controller
from pynput.keyboard import Key, Listener
import cv2 as cv
import numpy as np
cvNet = cv.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'graph.pbtxt')
controller = ai2thor.controller.Controller()
controller.start()
controller.reset('FloorPlan28')
event=controller.step(dict(action='Initialize', gridSize=0.25))
while True:
    img =  event.cv2img.copy()
    rows = img.shape[0]
    cols = img.shape[1]
    cvNet.setInput(cv.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))
    cvOut = cvNet.forward()
    for detection in cvOut[0,0,:,:]:
        score = float(detection[2])
        if score > 0.3:
            left = detection[3] * cols
            top = detection[4] * rows
            right = detection[5] * cols
            bottom = detection[6] * rows
            cv.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (23, 230, 210),thickness=2)
    cv.imshow('img', img)
    key=cv.waitKey(0)
    if key == 119:
    	event = controller.step(dict(action = 'MoveAhead'))
    if key == 115:
    	event = controller.step(dict(action = 'MoveBack'))
    if key == 97:
    	event = controller.step(dict(action = 'MoveLeft'))
    if key == 100:
    	event = controller.step(dict(action = 'MoveRight'))
    if key == 106:#j
     	event = controller.step(dict(action='RotateLeft'))
    if key == 108:#l
    	event = controller.step(dict(action='RotateRight'))
    if key == 105:#i
     	event = controller.step(dict(action='LookUp'))
    if key == 107:#k
    	event = controller.step(dict(action='LookDown'))
    if key ==27:
        break
