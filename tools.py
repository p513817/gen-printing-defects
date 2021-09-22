import numpy as np
import cv2
import random

from numpy.lib.function_base import angle

def gaussian(area, mean=0, sigma=0.8):
    """
    mean 均值, sigma 標準差
    輸出縮限到0~1之間
    """
    noise = np.random.normal(mean, sigma, area)
    return np.clip(noise, 0, 1)

def bgr2gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def bgr2bin(img, thresh):
    im_gray = bgr2gray(img)
    return cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

def erode(img):
    kernel = np.ones((3,3), np.uint8)
    erosion = cv2.erode(img, kernel, iterations = 1)
    return erosion

def dilate(img):
    kernel = np.ones((1,1), np.uint8)
    dilation = cv2.dilate(img, kernel, iterations = 1)
    return dilation

def is_rgb(img):
    return True if len(img.shape)==3 else False

def ez_randint(min, max):
    return np.random.randint(min, max)

def rand_noise(img, prob=1):
    """
    Generate random noise
    """
    h,w = img.shape[:2]

    noise_img = img.copy()
    noise_nums = int(prob*h*w)

    for i in range(noise_nums):
        row=ez_randint(0, h-1)
        col=ez_randint(0, w-1)

        if ez_randint(0,2)==0:
            noise_img[row, col]=255
        else:
            noise_img[row, col]=0
    return noise_img


def concate(s1, s2):    
    """
    auto concate images with same shape
    """
    s1_h, s1_w = s1.shape[:2]   
    return np.vstack((s1, s2)) if s1_h < s1_w else np.hstack((s1, s2))

def img_process(img, angle, resize, move, info=True):
    # warpAffine
    temp = img.copy()
    rows, cols = temp.shape[:2]
    

    # 旋轉 縮放
    M = cv2.getRotationMatrix2D( (cols//2, rows//2), angle, resize)
    temp = cv2.warpAffine(temp, M, (cols,rows), borderValue=0)    # 填充黑色

    # 平移
    M = np.float32([ [1, 0, move['x'] ], [ 0, 1, move['y']] ])
    temp = cv2.warpAffine(temp, M, (cols,rows), borderValue=0)    # 填充黑色

    if info:
        txt = "\n Angle: {},\n Resize: {},\n Move: {}, {}, \n".format( angle,
                                                                        resize,
                                                                        move['x'],
                                                                        move['y'])
        print(txt)

    return temp

def rand_area(img):
    h,w,c = img.shape
    nodes = ez_randint(3, 100)
    area = [[]]
    for idx in range(0, nodes):
        node_y = ez_randint(0,h)
        node_x = ez_randint(0,w)
        area[0].append([node_x, node_y])

    return np.array(area, dtype=np.int32)

def gen_mask(img):
    area = rand_area(img)
    mask = np.zeros(img.shape[:2], dtype="uint8")
    
    cv2.polylines(mask, area, 1, 255)
    cv2.fillPoly(mask, area, 255)

    return mask
