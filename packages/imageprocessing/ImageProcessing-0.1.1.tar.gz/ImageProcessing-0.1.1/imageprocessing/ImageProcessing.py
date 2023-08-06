
import numpy as np
import cv2
import sys

#cv2.namedWindow('image', cv2.WINDOW_NORMAL)

#Load the Image


def varInit():
    superimg = cv2.imread(sys.argv[1])
    imgo = cv2.imread(sys.argv[2])
    height, width = imgo.shape[:2]
    mask = np.zeros((height,width),np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    rect = (500,20,width-400,height-40)



    return (superimg,imgo,mask,rect,bgdModel,fgdModel,width,height)

def action(superimg,imgo,mask,rect,bgdModel,fgdModel,width,height):
    cv2.grabCut(imgo,mask,rect,bgdModel,fgdModel,2,cv2.GC_INIT_WITH_RECT)
    mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img1 = imgo*mask[:,:,np.newaxis]
    background = imgo - img1
    background[np.where((background > [0,0,0]).all(axis = 2))] = [255,255,255]
    return np.where((background == [255,255,255]),superimg,img1)


def almostMain():
    varss = varInit()
    superFinal = action(*varss)


    #image = cv2.rectangle(superFinal, (varss[3][0],varss[3][1]), (varss[3][2],varss[3][3]), (0,0,0), 2) 

    return superFinal
    
    

def main():
    import time
    

    image = almostMain()

    cv2.imshow('image', image) 

    k = cv2.waitKey(100)

    time.sleep(50)

    if k==27:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()


