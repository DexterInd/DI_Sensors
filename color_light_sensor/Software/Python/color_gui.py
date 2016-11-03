import pygame
from pygame.locals import *
import time
import TCS34725
import smbus

tcs = TCS34725.TCS34725(integration_time=TCS34725.TCS34725_INTEGRATIONTIME_154MS,gain=TCS34725.TCS34725_GAIN_16X)

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
    
    red, green, blue, c = tcs.get_raw_data()
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
        print('{0} {1} {2}'.format(r,g,b))
        screen.fill(background_color) #<--- Here
        pygame.display.update()
    time.sleep(.01)