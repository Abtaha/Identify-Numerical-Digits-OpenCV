import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import imutils


try:
    img = input("Enter your path to the image >> ")

    samples = np.loadtxt('models/X.data',np.float32)
    responses = np.loadtxt('models/y.data',np.float32)
    responses = responses.reshape((responses.size,1))

    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)

    im = cv2.imread(img)
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)

    contours = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    for cnt in contours:
        if cv2.contourArea(cnt) > 100:
            [x,y,w,h] = cv2.boundingRect(cnt)
            if  h > 90:
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                roi = thresh[y:y+h,x:x+w]
                roismall = cv2.resize(roi,(10,10))
                roismall = roismall.reshape((1,100))
                roismall = np.float32(roismall)
                retval, results, neigh_resp, dists = model.findNearest(roismall, k = 1)
                string = str(int((results[0][0])))
                cv2.putText(im, string, (x, y), 0, 1, (0,0,255), 3)

    cv2.imshow('im',im)
    cv2.waitKey(0)
except:
    print("Error")