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


#  a lot is being added here
class Model(object):
    # inits a custom number of bodies at semi-random positions inside screen
    def __init__(self, num_bodies=3, body_rad=10):
        self.bodies = []
        self.body_centers = []
        global screen_size
        screen_width, screen_height = screen_size

        while len(self.body_centers) < num_bodies:
            x = random.randint(0+body_rad, screen_width-body_rad)
            y = random.randint(0+body_rad, screen_height-body_rad)
            print x, y
            new_center = Point(x, y)
            if not self.too_close(new_center, self.body_centers, 2*body_rad):
                self.body_centers.append(new_center)

        for center in self.body_centers:
            self.bodies.append(Body(center.pos(), body_rad))

        print self.body_centers

        # self.body = Body((size[0]/2, size[1]/2), 50)

    def update(self):
    	global frame_rate
        for body in self.bodies:
            body.update(flag)
            if flag == 0: # a flag that identifies the B-key motion
            	pass
            elif flag == frame_rate:
            	pass 
            else: 
            	flag += 1
            	def explode(self,body):
            		""" Take current pos tuple,
            			create list of tuples of len(frame_rate)
            			to determine the explosion motion
            			where final pos is the initial pos tuple
            		"""
				    # center_screen = Point(250,250) # center of screen (hardcoded for now)
				    # x_dist = body.center.x - center_screen.x # current x distance of point from center
				    # y_dist = body.center.y - center_screen.y # current x distance of point from center
				    # if x_dist == 0:
				    #     x_dist_m = div_dis
				    # else:
				    #     x_dist_m = div_dis / x_dist # distance we move point from its recent location
				    # if y_dist == 0:
				    #     y_dist_m = div_dis
				    # else:
				    #     y_dist_m = div_dis / y_dist

				    # new_x = x_dist_m + body.center.x
				    # new_y = y_dist_m + body.center.y

				    # return (new_x, new_y)


    def too_close(self, new_point, points, distance):
        '''checks to see if the new_point is too close to any points in points
        '''
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
    def __init__(self, pos, rad, vel=(0.5, 0.0)):
        '''pos is cartesian, vel is (magnitude, theta)'''
        self.rad = int(rad)
        self.center = Point(*pos)
        self.vel = Vector(*vel)
        self.vel.base_vel = vel[0]
        # TODO
        self.vel.t = random.uniform(0, 2*math.pi)
        self.acc = Vector(0.0, 0.0)
        self.animate = False
        self.p_center = Point(*pos)
        self.flag = 0

    # ball will move with constant velocity, smoothly varying direction
    def update(self):
        if self.animate:

            self.acc.t = (3*self.acc.t + random.uniform(-0.1, 0.1)) / 4
            self.vel.t += self.acc.t

            # TODO Fix!!!
            global screen_size
            screen_width, screen_height = screen_size
            if self.center.x < 0 + self.rad:
                self.vel.t = math.pi - self.vel.t
                self.p_center.x = float(0 + self.rad)
            elif self.center.x > screen_width - self.rad:
                self.vel.t = math.pi - self.vel.t
                self.p_center.x = float(screen_width - self.rad)
            if self.center.y < 0 + self.rad:
                self.vel.t = 0 - self.vel.t
                self.p_center.y = float(0 + self.rad)
            elif self.center.y > screen_height - self.rad:
                self.vel.t = 0 - self.vel.t
                self.p_center.y = float(screen_height - self.rad)

            self.p_center.x += self.vel.m * math.cos(self.vel.t)
            self.p_center.y += self.vel.m * math.sin(self.vel.t)
            self.center.x = int(round(self.p_center.x))
            self.center.y = int(round(self.p_center.y))

            self.vel.m = (7*self.vel.m + self.vel.base_vel)/8


class PyGameWindowView(object):
    def __init__(self, model, screen):
        # self.model = model
        self.screen = screen

    def draw(self, model):
        # paint background
        self.screen.fill((20, 20, 20))  # (255, 32, 103))

        # draw every body in bodies
        for body in model.bodies:
            circle_png = pygame.image.load('circle.png')
            # circle = pygame.transform.scale(circle_png, (10,10))
            self.screen.blit(circle_png, 
                            (body.center.x -5,
                            body.center.y -6 )
                            )

        centers_list = [body.center.pos() for body in model.bodies]

        # draw joining lines
        if len(model.bodies) > 1:
	        pygame.gfxdraw.aapolygon(
	            self.screen,
	            centers_list,
	            (100, 100, 100, 100)
	            )

        pygame.display.update()


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
        self.snap_vertical = True

    def handle_event(self, event, model):
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
            self.speed_random(model)
        elif event.key == pygame.K_s:
            audio_unit.play_sample_num(1)
            self.speed_random(model)
        elif event.key == pygame.K_d:
            audio_unit.play_sample_num(2)
            self.speed_random(model)
        elif event.key == pygame.K_b:
            audio_unit.play_sample_num(3)
            for body in model.bodies:
            	body.flag = 1

        #  space quits for speed in testing
        elif event.key == K_SPACE:
            global running
            running = False
        else:
            return

    def speed_random(self, model, velocity=20.0, spin=1.0):
        target = random.choice(model.bodies)
        target.vel.m = velocity
        target.acc.t = spin * random.choice((1, -1))

if __name__ == '__main__':
    try:
        pygame.quit()
    except:
        pass

    pygame.init()
    frame_rate = 10
    screen_size = (500, 500)
    background = pygame.display.set_mode(screen_size)

    model = Model(1, 0)
    audio_unit = PyGameAudio()
    view = PyGameWindowView(model, background)
    controller = PyGameKeyboardController(model, audio_unit)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event, model)

        model.update()
        view.draw(model)
        time.sleep(1/frame_rate)

    pygame.quit()
