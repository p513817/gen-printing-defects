import numpy as np
import cv2

def draw_text(img, txt):

    cv2.putText(img, txt, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(img, txt, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    
class SelectAera:

    def __init__(self, img, WIN_NAME='RESULT'):

        self.img = img
        rows, cols = img.shape[:2]
        self.img_draw = img.copy()
        self.WIN_NAME = WIN_NAME

        #滑鼠按下為真
        self.drawing = False 
        self.mode = True

        self.ix = self.iy = self.px = self.py = -1
        self.bgr = []

        # initial
        cv2.namedWindow(self.WIN_NAME)
        cv2.setMouseCallback(self.WIN_NAME,self.draw_rectangle)
        
        img_temp = self.img.copy()
        draw_text(img_temp, "1. Drag to select area.")
        cv2.imshow(self.WIN_NAME,img_temp)


    def draw_rectangle(self, event, x, y, flags, param):
        
        img_temp = self.img.copy()

        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy= x, y

            draw_text(img_temp, "1. Drag to select area.")
            cv2.imshow(self.WIN_NAME,img_temp)

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing :
                cv2.rectangle(img_temp,(self.ix, self.iy),(x,y),(0,0,255),2)
                cv2.imshow(self.WIN_NAME,img_temp)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            cv2.rectangle(img_temp,(self.ix, self.iy),(x,y),(0,0,255),2)
            self.px, self.py=x, y
            self.img_draw = img_temp.copy()

            draw_text(img_temp, "2. Right click to select color.")
            cv2.imshow(self.WIN_NAME,img_temp)
        
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.bgr = img_temp[y, x]
            draw_text(self.img_draw, "3. Press 'q' to continue.")
            cv2.imshow(self.WIN_NAME,self.img_draw)

    def get_area(self):
        """
        Return x1,y1,x2,y2,bgr
        """

        while(True):    

            k = cv2.waitKey(0)

            if k == ord('q') or k==27:
                print('stop select area.')
                break
            elif k==ord('m'):
                if self.mode:
                    print("cancel mouse callback")
                    cv2.setMouseCallback(self.WIN_NAME, lambda *args : None ) 
                else:
                    print("setup mouse callback")    
                    cv2.setMouseCallback(self.WIN_NAME,self.draw_rectangle)
                self.mode = not self.mode
            elif k==ord('c'):
                print("clear rectangle")
                self.ix = self.iy = self.px = self.py = -1
                cv2.imshow(self.WIN_NAME, self.img)
                
        # cv2.destroyAllWindows()
        cv2.setMouseCallback(self.WIN_NAME, lambda *args : None )
        return self.ix, self.iy, self.px, self.py, self.bgr

if __name__=='__main__':
    img = cv2.imread('ok.jpg')
    event = SelectAera(img)
    res = event.get_area()
    print(res)