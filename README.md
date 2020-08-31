# totem
![totem logo](figures/totem_logo.png)
A Two Dimensional Barcode Optimized for Quick Detection

## Introduction
totem is a new type of barcode designed to be quickly parsed and easily detected. Other barcode formats like QR rely on clunky marking that aren't easily found
by detection software. totem solves this problem by being a circle. Circles are shapes that are extremely easy and quick to find. It also has a simple layout
which is easy to parse.

## How Does totem Work?
A totem is made up of rings which are made up of sectors. Each sector in a totem has the same area (thus the "information density" is constant throughout). A totem
has 5 data rings and an outer alignment ring. Each succsessive ring has two additional sectors so to keep each sector with the same area. Each sector represents one
bit of data. 

The lsb if the center ring. The next sector has the second and third bits, organized in the clockwise direction. As you march out to the next ring, you start at the 
top (as if it were a clock) and move clockwise. In total a totem can hold 25 bits (however I am currently working on implementing error correction, so expect
closer to 20 usuable bits).

## How does a totem detector work
Detecting a totem is simple. You first search for circles in the image (I am using a Hough Circle Detection Algorithm) and then you verify that the circle you found
is a totem by checking that roughly 1/6 of the outer ring is white and the other 5/6 is black.
