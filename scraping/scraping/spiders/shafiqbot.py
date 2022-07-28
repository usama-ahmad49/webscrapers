import math
import random
import pyautogui as pe
import numpy as np
import pygame
from scipy import interpolate
import time
import os
import subprocess




headers = ['X','Y','T','targX','targY']


def genratecircle(xbutton,ybutton):
    pygame.draw.circle(window, (0, 255, 0),[xbutton, ybutton], 10, 0)
    pygame.display.update()

def randomcordinates():
    xbutton = random.randint(10,screenHeight-100)
    ybutton = random.randint(10,screenWidth-20)
    return xbutton,ybutton


def point_dist(x1,y1,x2,y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def moveincurve(xbutton,ybutton):
    T = random.randint(1,3)
    angle = 360/360
    currentangle = 0
    cursorPosition = pe.position()
    # cursorPosition = (100,100)
    diameter = math.sqrt(math.pow((cursorPosition[0] - xbutton),2) + math.pow((cursorPosition[1] - ybutton),2))
    R = diameter//2
    x = []
    y = []
    for i in range(180):
        # x.append((R*(1/2*math.cos(i))) + xbutton)
        # y.append((R*(1/2*math.sin(i))) + ybutton)
        x.append(cursorPosition[0] + R*math.cos(math.radians(currentangle)))
        y.append(cursorPosition[1] + R*math.sin(math.radians(currentangle)))
        currentangle +=angle

    for i in range(x.__len__()):
        pe.moveTo(x[i],y[i], duration = 0.05)
#     cp = random.randint(3, 5)  # Number of control points. Must be at least 2.
#     x1, y1 = pe.position()  # Starting position
#
#     # Distribute control points between start and destination evenly.
#     x = np.linspace(x1, xbutton, num=cp, dtype='int')
#     y = np.linspace(y1, ybutton, num=cp, dtype='int')
#
#     # Randomise inner points a bit (+-RND at most).
#     RND = 10
#     xr = [random.randint(-RND, RND) for k in range(cp)]
#     yr = [random.randint(-RND, RND) for k in range(cp)]
#     xr[0] = yr[0] = xr[-1] = yr[-1] = 0
#     x += xr
#     y += yr
#
#     # Approximate using Bezier spline.
#     degree = 3 if cp > 3 else cp - 1 # Degree of b-spline. 3 is recommended.
#     # Must be less than number of control points.
#     tck, u = interpolate.splprep([x, y], k=degree)
#     # Move upto a certain number of points
#     u = np.linspace(0, 1, num=2 + int(point_dist(x1, y1, xbutton, ybutton) / 50.0))
#     points = interpolate.splev(u, tck)
#
#     # Move mouse.
#     duration = 0.1
#     timeout = duration / len(points[0])
#     point_list = zip(*(i.astype(int) for i in points))
#     for point in point_list:
#         pe.moveTo(*point)
#         time.sleep(0.5)


def movestringline(xbutton,ybutton):
    T = random.randint(1,5)
    pe.click(xbutton, ybutton, duration=T)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                window.fill((255, 255, 255))
                pygame.display.update()
if __name__ == '__main__':
    screenWidth, screenHeight = pe.size()
    #initlize pygame window for circle
    pygame.init()
    window = pygame.display.set_mode((screenWidth, screenHeight))
    window.fill((255, 255, 255))
    i=0
    while i<1:
        xbutton, ybutton = randomcordinates()
        genratecircle(xbutton,ybutton)
        xbutton,ybutton = 500,500
        moveincurve(xbutton, ybutton)
        # movestringline(xbutton,ybutton)
        i+=1





