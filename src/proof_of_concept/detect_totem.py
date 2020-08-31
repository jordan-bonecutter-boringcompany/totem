# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# detect_totem.py # # # # # # # # # # # # # # # # # # # # # # #
# created by: jordan bonecutter for The Boring Company# # # # #
# contact: jpbonecutter@gmail.com # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import cv2 as cv
import numpy as np
import math


_detect_size = 200
_ring_samples = 60


def detect_totem(image):
  '''
  Returns a list of subimages where totems were detected
  '''

  # convert the image to gray for edge detector
  gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
  gray = cv.blur(gray, (3, 3))

  # find circles using Hough Circle detection
  circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 5, param1=100, param2=50, minRadius=10, maxRadius=50)
  circles = np.uint16(np.around(circles))
  totems = []
  if circles is None: 
    return None

  # for each circle, check if its a totem by looking at
  # the outer ring and seeing if the ratio of white to black
  # pixels is nearly 1:5
  for circle in circles[0]:
    cx, cy, r = circle
    white_pix = 0
    black_pix = 0
    # sample around the ring
    for sample in range(_ring_samples):
      avg_color = np.zeros(3)
      theta = (sample / _ring_samples) * 2*math.pi
      # sample multiple shells
      for dr in range(int(r/6)):
        x = cx + (r - dr)*math.cos(theta)
        y = cy + (r - dr)*math.sin(theta)
        avg_color += image[int(y), int(x)]
      # determine average color at sample
      # if it's < 127 then it's black
      # otherwise it's white
      avg_color /= int(r/6)
      avg_color = np.average(avg_color)
      if avg_color > 127:
        white_pix += 1
      else:
        black_pix += 1
    # check if the amount of white pixels is roughly 1/6 of the total
    if (1/7) < (white_pix / (black_pix + white_pix)) < (1/5):
      totems.append(circle) 

  # create subimage of current totem
  ret = []
  for totem in totems:
    curr = np.zeros((_detect_size, _detect_size, 3), dtype=np.uint8)
    ret.append(curr)
    cx, cy, r = int(cx), int(cy), int(r)
    for y in range(_detect_size):
      yprime = int(cy + ((y / (_detect_size - 1)) - 0.5)*2*r)
      for x in range(_detect_size):
        xprime = int(cx + ((x / (_detect_size - 1)) - 0.5)*2*r)
        curr[y, x] = image[yprime, xprime]

  return ret


def main():
  image = cv.imread('../../images/totem_testimage10.png')
  detected = detect_totem(image)
  if detected is None:
    print('No totems found')
    return 0

  for n, detection in enumerate(detected):
    cv.imwrite('../../images/detected.png', detection)
  
if __name__ == '__main__':
  main()
