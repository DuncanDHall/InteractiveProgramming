""" Figuring out how the point will move""" 

import pygame
from pygame.locals import *
import time
import random
import glob
import math
from pygame import gfxdraw

# links:
# https://www.cs.ucsb.edu/~pconrad/cs5nm/topics/pygame/drawing/


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def pos(self):
        return self.x, self.y


class Vector(object):
    def __init__(self, magnitude, theta):
        self.m = magnitude
        self.t = theta


class Body(object):
    def __init__(self, pos, rad, vel=(0.5, 0.0)):
        '''pos is cartesian, vel is (magnitude, theta)'''
        self.rad = int(rad)
        self.center = Point(*pos)
        self.vel = Vector(*vel)
        self.vel.base_vel = vel[0]
        self.vel.t = random.uniform(0, 2*math.pi)
        self.acc = Vector(0.0, 0.0)
        self.animate = True
        self.p_center = Point(*pos)

def draw(self):
        # paint background
        self.screen.fill((20, 20, 20))  # (255, 32, 103))
        # draw every body in bodies
	    circle_png = pygame.image.load('circle.png')
	        # circle = pygame.transform.scale(circle_png, (10,10))
	        self.screen.blit(circle_png, 
	                        (body.center.x -5,
	                        body.center.y -6 )
	                        )

        centers_list = [body.center.pos() for body in model.bodies]

        # draw joining lines
        pygame.gfxdraw.aapolygon(
            self.screen,
            centers_list,
            (100, 100, 100, 100)
            )

        pygame.display.update()



 if __name__ == '__main__':
    try:
        pygame.quit()
    except:
        pass

    pygame.init()

    screen_size = (500, 500)
    background = pygame.display.set_mode(screen_size)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)

        time.sleep(0.01)

    pygame.quit()
