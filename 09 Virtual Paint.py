import cv2
import numpy as np

frameWidth = 640
frameHeigth = 480

cap = cv2.VideoCapture(0)

cap.set(3,frameWidth)
cap.set(4,frameHeigth)
cap.set(10,150)

#definos los colores a utilizar buscandolos como en la leccion 07
myColorsMask = [[0,3,195,255,104,255],#rojo
                [103,115,185,255,81,178],#azul
                [57,93,163,255,137,219]]#verde
                
colorsPaint = [[80,175,76],#verde
               [0,0,213],#rojo
               [161,71,13]]#azul

puntos = []#Coleccion de ounto totales:  x,y,color

def drawCanvas(img,puntos):
    for punto in puntos:
        cv2.circle(img,(punto[0],punto[1]),5,punto[2],cv2.FILLED)


def getContours(img,mask,colorPaint):
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for c in contours:
        area = cv2.contourArea(c)   
        
        #cv2.drawContours(imgContour,c,-1,(255,0,0),3)
        peri = cv2.arcLength(c,True)#calcula la longitud del contorno o curva
        
        approx = cv2.approxPolyDP(c,0.02*peri,True)#calcula los vertices
        objCor = len(approx)#numero de vertices
        x,y,w,h = cv2.boundingRect(approx) #bounding box
        if area>100:
            #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)#pintamos el bounding box
            cv2.circle(img,(x+w//2,y),5,colorPaint,5)
            puntos.append([x+w//2,y,colorPaint])
            break

def findColor(img,colors):
    
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)#hue saturation value
    for color in colors:
        lower = np.array([color[0],color[2],color[4]])
        upper = np.array([color[1],color[3],color[5]])
        mask = cv2.inRange(imgHSV,lower,upper)
        colorPaint = []
        if color == [0,3,195,255,104,255]: colorPaint = [0,0,213]#rojo
        elif color == [103,115,185,255,81,178]: colorPaint = [161,71,13]#Azul
        else: colorPaint = [80,175,76]#verde
        getContours(img,mask,colorPaint)
        #cv2.imshow(str(color[0]),mask)

while cap.isOpened():
    success, img = cap.read()
    if(len(puntos)>0):drawCanvas(img,puntos)
    findColor(img,myColorsMask)
    cv2.imshow('result',img)
    cv2.waitKey(1)



