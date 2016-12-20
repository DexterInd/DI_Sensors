#!/usr/bin/env python
#
# Python GUI example for the DI color sensor which shows color on the screen when the sensor is brought near a color
#
'''
## License
The MIT License (MIT)

Copyright (C) 2016  Dexter Industries
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
import pygame
from pygame.locals import *
import time
import di_color_sensor

cs = di_color_sensor.color_sensor() 

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)

i=0
background_color = (i,i,i)
(width, height) = (300, 300)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Color Test')
screen.fill(background_color)

pygame.display.flip()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    red, green, blue, c = cs.get_raw_colors()
    sum= c
    r = red*1.0
    r /= sum
    g = green*1.0
    g /= sum
    b = blue*1.0
    b /= sum
    r *= 256
    g *= 256
    b *= 256
    r = int(r)
    g = int(g)
    b = int(b)
    l=[r,g,b]
    if r<256 and g<256 and b<256:
        background_color = (r,g,b)
        print('r:{0} g:{1} b:{2}'.format(r,g,b))
        screen.fill(background_color) #<--- Here
        pygame.display.update()
    time.sleep(.01)