import numpy as np
import cv2
import os

import sys
import time

datasets = 'detected'

path = os.path.join(datasets)
(width, height) = (130, 100)







fire_cascade = cv2.CascadeClassifier('fire_detection.xml')
#fire_detection.xml file & this code should be in the same folder while running the code

cap = cv2.VideoCapture(0)
while 1:
    
    ret, img = cap.read()
    
    ##Gaussian Blurring
    kernel = np.ones((7,7),np.float32)/25
    img1 = cv2.filter2D(img,-1,kernel)
    cv2.imshow('Gaussian',img1)

    ## Bilateral Filter for Edge Enhancement
    img3 = cv2.bilateralFilter(img1,9,75,75)
    cv2.imshow('Bilateral',img3)
    
##    cv2.imshow('imgorignal',img)
    gray = cv2.cvtColor(img3,cv2.COLOR_BGR2GRAY)
    cv2.imshow('Grayscale',gray)
    
    fire = fire_cascade.detectMultiScale(gray, 1.2, 5)
    a=str(fire)
   
    for (x,y,w,h) in fire:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        if a>='302 322  61  61' :
            count = 1
            while count < 60:
                img_resize = cv2.resize(roi_color, (width, height))
                cv2.imwrite('%s/%s.jpg' % (path,count), img_resize)
                count += 1
            print ('Fire is detected..!')
            cv2.imwrite("first.jpg",img)
            
        time.sleep(0.2)
        
    cv2.imshow('img',img)
    
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
