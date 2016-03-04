import pygame
from pygame.locals import *
import time
import random
import glob
import math

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


#  a lot is being added here
class Model(object):
    # inits a custom number of bodies at semi-random positions inside screen
    def __init__(self, screen=(375, 467), num_bodies=3, body_rad=40):
        self.bodies = [ ] 
        self.body_centers = [ ]

        while len(self.body_centers) < num_bodies:
            x = random.randint(0+body_rad, screen[0]-body_rad)
            y = random.randint(0+body_rad, screen[1]-body_rad)
            print x, y
            new_center = Point(x, y)
            if not self.too_close(new_center, self.body_centers, 2*body_rad):
                self.body_centers.append(new_center)

        for center in self.body_centers:
            self.bodies.append(Body(center.pos(), body_rad))

        print self.body_centers

        self.body = Body((size[0]/2, size[1]/2), 50)

    def update(self):
        for body in self.bodies:
            body.update()

    def too_close(self, new_point, points, distance):
        '''checks to see if the new_point is too close to any points in points'''
        if not points:
            return False
        for point in points:
            if math.hypot(
                    point.x - new_point.x,
                    point.y - new_point.y
                    ) < distance:
                return True
        return False


class Body(object):
    def __init__(self,pos,rad,vel=(2, 0.0)):
        '''pos is cartesian, vel is (magnitude, theta)'''
        self.rad = rad
        self.center = Point(*pos)
        self.vel = Vector(*vel)
        self.acc = Vector(0.0, 0.0)
        self.animate = True

    # ball will move with constant velocity, smoothly varying direction
    def update(self):
        if self.animate:
            self.acc.t += random.uniform(-0.01, 0.01)
            self.vel.t += self.acc.t
            self.center.x += int(round(self.vel.m * math.cos(self.vel.t)))
            self.center.y += int(round(self.vel.m * math.sin(self.vel.t)))


class PyGameWindowView(object):
    def __init__(self, model, screen):
        # self.model = model
        self.screen = screen

    def draw(self, model):
        self.screen.fill(pygame.Color(255, 32, 103))
        # draw every body in bodies
        for body in model.bodies:
            pygame.draw.circle(
                self.screen,
                pygame.Color(0,0,0),
                body.center.pos(),
                body.rad,
                5
            )

        pygame.display.update()
        print 'drawn'

    def update(self):
        pass



class PyGameAudio(object):
    def __init__(self):
        # get paths for all .wavs in sounds flolder
        self.sound_paths = glob.glob('sounds/*.wav')
        print self.sound_paths  # SUB

    def play_sample_num(self, index):
        sound = pygame.mixer.Sound(self.sound_paths[index])
        sound.play()


class PyGameKeyboardController(object):
    def __init__(self, model, audio_unit):
        self.model = model

    def handle_event(self, event):
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            print 'do something when left arrow is pressed'
        elif event.key == pygame.K_RIGHT:
            print 'right'
        #  different method of playing samples.
        #   Now audio_unit handles everything
        elif event.key == pygame.K_a:
            audio_unit.play_sample_num(0)
        elif event.key == pygame.K_s:
            audio_unit.play_sample_num(1)
        #  space quits for speed in testing
        elif event.key == K_SPACE:
            global running
            running = False
        else:
            return


if __name__ == '__main__':
    try:
        pygame.quit()
    except:
        pass

    pygame.init()

    size = (375, 467)
    screen = pygame.display.set_mode(size)

    model = Model()
    audio_unit = PyGameAudio()
    view = PyGameWindowView(model, screen)
    controller = PyGameKeyboardController(model, audio_unit)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)

        model.update()
        view.draw(model)
        time.sleep(0.01)

    pygame.quit()
