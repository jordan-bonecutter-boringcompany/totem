# totem - A Light 2 Dimensional Barcode
<img src="figures/totem_logo.png" width="250">

## Introduction
totem is a new type of barcode designed to be quickly parsed and easily detected. Other barcode formats like QR rely on clunky markings that aren't so easy to find. totem solves this problem by being circular. Circles are extremely easy and quick to find via algorithms like Hough Circle detection.
which is easy to parse.

## How Does totem Work?
A totem is made up of rings which are made up of sectors. Each sector in a totem has the same area (thus the "information density" is constant throughout). A totem
has 5 data rings and an outer alignment ring. Each succsessive ring has two additional sectors so to keep each sector with the same area. Each sector represents one
bit of data. 

The lsb is coded in the center ring. The next sector has the second and third bits, organized in the clockwise direction. As you march out to the next ring, you start at the 
top (as if it were a clock) and move clockwise. In total a totem can hold 25 bits (however I am currently working on implementing error correction, so expect
closer to 20 usuable bits).

## How Does a totem Detector Work?
Detecting a totem is simple. You first search for circles in the image (I am using a Hough Circle Detection Algorithm) and then you verify that the circle you found
is a totem by checking that roughly 1/6 of the outer ring is white and the other 5/6 is black.

## How Does a totem Decoder Work?
Given a totem subimage found by the totem detector, the decoder first moves into polar coordinates. Polar coordinates make dealing with the ringed structure far simpler. Now it has a sample 2D data matrix which can be divided into a grid. The value of the bit will be the average value in the grid at that point.
