# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# detect_totem.py # # # # # # # # # # # # # # # # # # # # # # #
# created by: jordan bonecutter for The Boring Company# # # # #
# contact: jpbonecutter@gmail.com # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import cv2 as cv
import numpy as np
import math


DETECT_SIZE = 200


def detect_totem(image):
  image_copy = image.copy()
  gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
  gray = cv.blur(gray, (3, 3))
  circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 5, param1=100, param2=50, minRadius=10, maxRadius=50)
  if circles is None:
    return None
  circles = np.uint16(np.around(circles))
  cx, cy, r = circles[0][0]

  ret = np.zeros((DETECT_SIZE, DETECT_SIZE, 3), dtype=np.uint8)
  cx, cy, r = int(cx), int(cy), int(r)
  for y in range(DETECT_SIZE):
    yprime = int(cy + ((y / (DETECT_SIZE - 1)) - 0.5)*2*r)
    for x in range(DETECT_SIZE):
      xprime = int(cx + ((x / (DETECT_SIZE - 1)) - 0.5)*2*r)
      ret[y, x] = image[yprime, xprime]

  return ret


def main():
  image = cv.imread('images/totem_testimage10.png')
  detected = detect_totem(image)
  if detected is None:
    print('No totems found')
    return 0

  cv.imwrite('images/detected.png', detected)
  
if __name__ == '__main__':
  main()
