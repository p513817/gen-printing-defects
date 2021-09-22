import cv2
import numpy as np
import os
from numpy import random
from tools import gen_mask, img_process, rand_noise, ez_randint, concate
from cv_event import SelectAera
import argparse

"""
目標是將 ok 的圖添加 雜訊
1. 高斯 噪點
2. 直接透過隨機原點去增加雜訊 
"""

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--select", action="store_true", help="select the target area.")
parser.add_argument("-i", "--image", help="input images which you want to generate dust.")
parser.add_argument("-d", "--density", type=float, help="fix dust's density. value:0~1")
parser.add_argument("-o", "--output-dir", default='./output', help="output directory.")

args = parser.parse_args()

# Get Parser's Argument
path = args.image
density = args.density if args.density else False
save_path = args.output_dir

# Check Saving Directory is exist
if not os.path.exists(save_path):
    print('Creating save-dir: {} ... '.format(save_path), end='')
    os.mkdir(save_path)
    print('Done' if os.path.exists(save_path) else 'Failed')
        
# Get Image and Information 
img_org = cv2.imread(path)
rows, cols = img_org.shape[:2]

save_idx = 0
x1, y1, x2, y2 = 0, 0, rows, cols

if args.select:
    event = SelectAera(img_org)
    x1, y1, x2, y2 = event.demo()

while(True):

    img_temp = img_org.copy()
    
    # Get Mask
    mask = gen_mask(img_temp)

    # Get Mask with noise
    den = density if density else ez_randint(10,100)/100
    white_bg = np.zeros(img_temp.shape, dtype="uint8")
    noise = rand_noise(white_bg, den)
    
    mask_noise = cv2.bitwise_and(noise, noise, mask=mask)

    # Image Processing
    angle = ez_randint(0,360)
    resize = ez_randint(10, 80)/100
    move = {'x':ez_randint(cols*-1, cols)/2,'y':ez_randint(rows*-1, rows)/2 }

    # Crop Target Area
    mask_final = img_process(mask_noise, angle, resize, move, info=False)[y1:y2,x1:x2]
    
    # Border to Same Size
    mask_final = cv2.copyMakeBorder(mask_final, y1-0, rows-y2, x1-0, cols-x2, cv2.BORDER_CONSTANT,value=[0,0,0])
    
    # Add two image together
    result = cv2.add(mask_final, img_temp)
    
    # Show Result
    cv2.rectangle(mask_final,(x1, y1),(x2, y2),(0,0,255),2)
    cv2.imshow('result', concate(mask_final, result))

    key = cv2.waitKey(1)
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
