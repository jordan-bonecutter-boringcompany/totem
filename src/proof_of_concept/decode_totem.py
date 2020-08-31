# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# decode_totem.py # # # # # # # # # # # # # # # # # # # # # # #
# created by: jordan bonecutter for The Boring Company# # # # #
# contact: jpbonecutter@gmail.com # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import cv2 as cv
import numpy as np
import math
import statistics

def unwrap(image):
  '''
  Convert image to polar coordinates
  '''
  unwrapped = np.zeros(image.shape, dtype=np.uint8)
  for y in range(unwrapped.shape[0]):
    theta = (math.pi / 2) - (((y / unwrapped.shape[0]))*2*math.pi)
    for x in range(unwrapped.shape[1]):
      rho = ((unwrapped.shape[1])/2) * ((x / unwrapped.shape[1]))
      xprime = (rho * math.cos(theta)) + (unwrapped.shape[1] / 2)
      yprime = (unwrapped.shape[0] / 2) - (rho * math.sin(theta))
      unwrapped[y, x] = image[int(yprime), int(xprime)]
  return unwrapped


def read_totem(totem_image):
  '''
  Decodes image containing only the totem 
  '''

  # first convert the image to polar coords
  unwrapped = unwrap(totem_image) 

  # calculate ring thickness
  ring_thickness = unwrapped.shape[1] / 6

  # correctly align totem:
  # first find the center of the white area
  # this is done with a weighted average
  # then center the white area using numpy.roll
  ring = 5
  white_rows = 0
  n_white_rows = 0
  zero_white = False
  end_white = False
  for y in range(unwrapped.shape[0]):
    avg_color = np.average(unwrapped[y, int(ring_thickness*ring):int(ring_thickness*(ring+1))])
    if avg_color > 0.5*255:
      if y == 0:
        zero_white = True
      elif y == unwrapped.shape[0] - 1:
        end_white = True
      white_rows += y
      n_white_rows += 1

  # use numpy.roll to center the white area
  middle = white_rows / n_white_rows
  if zero_white and end_white:
    ydelta = 0.5*(unwrapped.shape[0]-1) - middle
    unwrapped = np.roll(unwrapped, int(ydelta))
  else:
    unwrapped = np.roll(unwrapped, -int(middle), axis=0)

  # iterate through each ring
  code = 0
  current_bit_id = 0
  for ring in range(5):
    xstart = int(ring_thickness*ring)
    xend   = int(ring_thickness*(ring+1))
    sector_length = unwrapped.shape[0]/(2*ring+1)
    for sector in range(2*ring + 1):
      # find the average color in the current sector
      ystart = int(sector*sector_length)
      yend   = int((sector+1)*sector_length)
      avg_color = np.average(unwrapped[ystart:yend, xstart:xend])

      # the current bit is 0 if the sector is black and
      # white otherwise
      current_bit = int((avg_color/255.) + 0.5)
      code |= current_bit << current_bit_id
      current_bit_id += 1

  return code


def main():
  image = cv.imread('images/detected.png')
  code = read_totem(image)
  print(code)


if __name__ == '__main__':
  main()

