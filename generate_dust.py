import cv2
import numpy as np
import os
from numpy import random
from tools import gen_mask, img_process, rand_noise, ez_randint, concate
from cv_event import SelectAera
import argparse
import sys

# Define Trackbar
def update(x):
    global den_max, den_min
    den_max = cv2.getTrackbarPos(TRACKBAR_NAME, WIN_NAME)

# Initial Argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--select", action="store_true", help="select the target area.")
parser.add_argument("-a", "--auto", action="store_true", help="auto gen mode ( for demo ).")
parser.add_argument("-i", "--image", help="input images which you want to generate dust.")
parser.add_argument("-d", "--density", type=float, help="fix dust's density. value:0~1")
parser.add_argument("-o", "--output-dir", default='./output', help="output directory.")
args = parser.parse_args()

# Get Parser's Argument
path = args.image
density = args.density if args.density else False
den_max = 100
den_min = 0
save_path = args.output_dir
wait_time = 1 if args.auto else 0

# Check Saving Directory is exist
if not os.path.exists(save_path):
    print('Creating save-dir: {} ... '.format(save_path), end='')
    os.mkdir(save_path)
    print('Done' if os.path.exists(save_path) else 'Failed')
        
# Get Image and Information 
img_org = cv2.imread(path)
rows, cols = img_org.shape[:2]

# Saving Images and Target Area Parameters
save_idx = 0
x1, y1, x2, y2 = 0, 0, rows, cols

# Initial OpenCV Windows
WIN_NAME = "RESULT"
TRACKBAR_NAME = "Setting Up Density of Defects"


cv2.namedWindow(WIN_NAME)
cv2.createTrackbar(TRACKBAR_NAME,WIN_NAME, 0, 100, update)
cv2.setTrackbarPos(TRACKBAR_NAME,WIN_NAME,80)


if args.select:
    event = SelectAera(img_org, WIN_NAME)
    
    x1, y1, x2, y2, bgr = event.get_area()
    
    if -1 in [x1,y1,x2,y2]:
        print('there is no area selected.')
        sys.exit(1)
    
while(True):

    img_temp = img_org.copy()
    
    # Get Mask
    mask = gen_mask(img_temp)

    # Get Mask with noise
    den = density if density else ez_randint(den_min,den_max)/100
    white_bg = np.zeros(img_temp.shape, dtype="uint8")
    noise_bg = rand_noise(white_bg, den)    # noise with 0, 255
    noise = cv2.bitwise_and(noise_bg, noise_bg, mask=mask)    

    # Image Processing
    angle = ez_randint(0,360)
    resize = ez_randint(10, 80)/100
    move = {'x':ez_randint(cols*-1, cols)/2,'y':ez_randint(rows*-1, rows)/2 }
    mask_final = img_process(noise, angle, resize, move, info=False)
    # Crop Target and Border to Same Size
    mask_final = mask_final[y1:y2,x1:x2]
    mask_final = cv2.copyMakeBorder(mask_final, y1-0, rows-y2, x1-0, cols-x2, cv2.BORDER_CONSTANT,value=[0,0,0])
    
    # Replace Pixel # Method 1
    result=np.where( mask_final<=10, img_temp, bgr)

    # Replace Pixel # Method 2
    # for r in range(rows):
    #     for c in range(cols):
    #         if np.sum(mask_final[r, c])>=10:
    #             img_temp[r, c]=bgr
    #         else:
    #             pass
    
    # Other way ( this way is easy and faster but got color problem)
    # Add two image together
    # result = cv2.add(mask_final, img_temp)
    
    # Show Result
    cv2.rectangle(mask_final,(x1, y1),(x2, y2),(0,0,255),2)
    cv2.imshow('RESULT', concate(mask_final, result))

    key = cv2.waitKey(wait_time)
    if key==ord('q'):
        break
    elif key==ord('s'):
        img_save = f'./output/output_{save_idx}.png'
        cv2.imwrite(img_save, result)
        print(f'Saved Image ({img_save})')
        save_idx += 1
    else:
        continue

    cv2.destroyAllWindows()
