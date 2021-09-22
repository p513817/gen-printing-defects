import numpy as np
import cv2

class SelectAera:

    def __init__(self, img):

        self.img = img

        #滑鼠按下為真
        self.drawing = False 
        self.mode = True

        self.ix, self.iy = -1, -1
        self.px,self.py = -1, -1

        # initial
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',self.draw_rectangle)
        cv2.imshow('image',self.img)

    def draw_rectangle(self, event, x, y, flags, param):
        
        img_temp = self.img.copy()

        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy= x, y
            cv2.imshow('image',img_temp)

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing :
                cv2.rectangle(img_temp,(self.ix, self.iy),(x,y),(0,0,255),2)
                cv2.imshow('image',img_temp)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            cv2.rectangle(img_temp,(self.ix, self.iy),(x,y),(0,0,255),2)
            self.px, self.py=x, y
            cv2.putText(img_temp, "PRESS 'q' TO CONTINUE.", (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(img_temp, "PRESS 'q' TO CONTINUE.", (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1, cv2.LINE_AA)

            cv2.imshow('image',img_temp)

    def get_cursor(self):
        return self.ix, self.iy, self.px, self.py

    def demo(self):

        while(True):    

            k = cv2.waitKey(1)

            if k == ord('q') or k==27:
                print('stop select area.')
                break
            elif k==ord('m'):
                if self.mode:
                    print("cancel mouse callback")
                    cv2.setMouseCallback('image', lambda *args : None ) 
                else:
                    print("setup mouse callback")    
                    cv2.setMouseCallback('image',self.draw_rectangle)
                self.mode = not self.mode
            elif k==ord('c'):
                print("clear rectangle")
                cv2.imshow('image', self.img)
                
        cv2.destroyAllWindows()
        return self.ix, self.iy, self.px, self.py

if __name__=='__main__':
    img = cv2.imread('ok.png')
    event = SelectAera(img)
    res = event.demo()
    print(res)