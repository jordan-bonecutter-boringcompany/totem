# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# generate_totem.py # # # # # # # # # # # # # # # # # # # # # #
# created by: jordan bonecutter for The Boring Company# # # # #
# contact: jpbonecutter@gmail.com # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import cairo
import numpy as np
import cv2 as cv
import math

class TotemGenerator:
  def __init__(self, size):
    self._resolution = (size, size, 4)
    self._data = np.zeros(self._resolution, dtype=np.uint8) 
    self._surface = cairo.ImageSurface.create_for_data(self._data, cairo.Format.RGB24, size, size)
    self._context = cairo.Context(self._surface)
    self._context.set_line_cap(cairo.LineCap.BUTT)

  def _clear(self):
    self._data[:] = 255

  def generate(self, code):
    '''
    Generate a totem for a code in the range 0 -> 32767

    @param code: int in the range 0 -> 32767
    '''
    # bits move outward and clockwise
    #
    # each sector has the same area, so each successive ring
    # has 2 more sectors than the previous.
    #
    # setup
    self._clear()
    current_bit_id = 0
    ring_thickness = 0.95*(self._resolution[0] / 12)
    self._context.set_line_width(1.01 * ring_thickness)
    center = (self._resolution[0] / 2, self._resolution[1] / 2)

    # iterate through each ring and sector
    for ring in range(1, 6):
      # calculate sector length in current ring
      d_theta = 2*math.pi / (2*ring - 1)
      for sector in range(2*ring - 1):
        # calculate the current bit using bitwise and
        current_bit = code & (0x1 << current_bit_id)  
        current_bit_id += 1

        # find start and end draw angle for current sector
        angle_start = sector * d_theta - math.pi / 2
        angle_end = (sector + 1) * d_theta - math.pi / 2

        # sectors with set bits have color 1 while
        # unset bits are black
        if current_bit:
          self._context.set_source_rgb(1, 1, 1)
        else:
          self._context.set_source_rgb(0, 0, 0)
        self._context.arc(center[0], center[1], ring_thickness * (ring - 0.5), angle_start, angle_end+0.01)
        self._context.stroke()

    # do outer ring
    self._context.set_source_rgb(0, 0, 0)
    self._context.arc(center[0], center[1], ring_thickness * 5.5,  - math.pi/2 + math.pi/6, -math.pi/2 - math.pi/6)
    self._context.stroke()
    return self._data


# test program
def main():
  generator = TotemGenerator(1500)
  totem = generator.generate(0b1110011000010100101101010)
  cv.imwrite('../../images/totem.png', totem)


if __name__ == '__main__':
  import cv2 as cv
  main()

