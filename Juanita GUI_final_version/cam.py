import cv2
import numpy as np

def draw(mask, color, frame_c):
  contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
      cv2.CHAIN_APPROX_SIMPLE)
  for c in contours:
    area = cv2.contourArea(c)
    if area > 1000:
      new_contour = cv2.convexHull(c)
      cv2.drawContours(frame_c, [new_contour], 0, color, 3)     

def capture(): 

  cap = cv2.VideoCapture(0)
  low_yellow = np.array([20,190,20],np.uint8)
  high_yellow = np.array([30,255,255],np.uint8)

  low_blue = np.array([85, 200, 20], np.uint8)
  high_blue = np.array([125, 255, 255], np.uint8)

  low_green = np.array([45, 100, 20], np.uint8)
  high_green = np.array([75, 255, 255], np.uint8)

  low_red1 = np.array([0,100,20],np.uint8)
  high_red1 = np.array([5,255,255],np.uint8)
  low_red2 = np.array([175,100,20],np.uint8)
  high_red2 = np.array([179,255,255],np.uint8)

  while True:
    comp,frame = cap.read()
    if comp == True:
      frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
      yellow_mask = cv2.inRange(frameHSV,low_yellow,high_yellow)
      blue_mask = cv2.inRange(frameHSV, low_blue, high_blue)
      green_mask = cv2.inRange(frameHSV, low_green, high_green)
      red_mask1 = cv2.inRange(frameHSV,low_red1,high_red1)
      red_mask2 = cv2.inRange(frameHSV,low_red2,high_red2)
      red_mask = cv2.add(red_mask1,red_mask2)
      draw(red_mask,(0,0,255), frame)
      draw(blue_mask, (255, 0, 0), frame)
      draw(green_mask,(0, 143, 57), frame)
      draw(yellow_mask,(35,220,240), frame)
      cv2.imshow('Webcam',frame)
            
      if cv2.waitKey(1) & 0xFF == ord('s'):
        break
        cap.release()
        cv2.destroyAllWindows()
  
