import pygame
from pygame.locals import *
import time
import random
import glob
import math
from pygame import gfxdraw


### FUTURE IMPLMENTATION:  Instead of trying to move bodies proportionally to each other and the center
### what if instead we captured the 'image' of the updated screen the moment the B-key is pressed. Then we could
### work with transformning the 'image' in relation to the coordinate system instead of the objects in 
### relation to each other (which we are doing currently) Hopefully that would help us get over some of our
### funky body math and get a smoother motion for the B-key event node expansion

class Point(object): 
    """ creating point class, to determine location of all our stuff 
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def pos(self):
        return self.x, self.y


class Vector(object):
    """ creating motion vectors class that describe movement of points
    """
    def __init__(self, magnitude, theta):
        self.m = magnitude
        self.t = theta


class Body(object):
    """ Defines bodies with center points, and dimensions,
        and initilizes behavior objects
    """
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
        self.next_positions = []
        self.flag = -1

    def update(self):
        """ This keeps all bodies on screen 
            as it moves them. Particular movements 
            for certain events are defined here
        """
        # debugging remenants: 
        # if self.flag != -1:
        #     import pdb; pdb.set_trace()

        # drifing animation only if our flag is down (= -1)
        # flag always begins as down
        # currently flag is raised when B-key is recognized as 
        # pressed in PygameKeyboardController objects
        if self.animate and self.flag == -1:

            self.acc.t = (3*self.acc.t + random.uniform(-0.1, 0.1)) / 4
            self.vel.t += self.acc.t

            global screen_size
            screen_width, screen_height = screen_size

            if self.center.x < 0 + self.rad: # Left side
                self.vel.t = math.pi - self.vel.t
                self.p_center.x = float(0 + self.rad)
            elif self.center.x > screen_width - self.rad: # Right side
                self.vel.t = math.pi - self.vel.t
                self.p_center.x = float(screen_width - self.rad)
            if self.center.y < 0 + self.rad: # Top
                self.vel.t = 0 - self.vel.t
                self.p_center.y = float(0 + self.rad)
            elif self.center.y > screen_height - self.rad: # Bottom
                self.vel.t = 0 - self.vel.t
                self.p_center.y = float(screen_height - self.rad)

            self.p_center.x += self.vel.m * math.cos(self.vel.t)
            self.p_center.y += self.vel.m * math.sin(self.vel.t)

            self.vel.m = (7*self.vel.m + self.vel.base_vel)/8 # playing with magnitue of vel 
        # catches case where animate is off but no flag
        elif self.flag == -1:
            pass
        # frame_rate is used to determine length of behavior given B-key press 
        # this keeps the flag raised until we reach the end of our framerate
        elif self.flag >= frame_rate -1:
            self.flag = -1
        # when flag raised
        else:
            # debuggy stuff
            # import pdb; pdb.set_trace()
            self.p_center.x, self.p_center.y = self.next_positions[self.flag]
            self.flag += 1

            global screen_size
            screen_width, screen_height = screen_size

            if self.p_center.x < -10 + self.rad:
                self.vel.t = math.pi - self.vel.t
                self.p_center.x = float(-10 + self.rad)
            elif self.p_center.x > screen_width - self.rad:
                self.vel.t = math.pi - self.vel.t
                self.p_center.x = float(10 + screen_width - self.rad)
            if self.p_center.y < -10 + self.rad:
                self.vel.t = 0 - self.vel.t
                self.p_center.y = float(-10 + self.rad)
            elif self.p_center.y > screen_height - self.rad:
                self.vel.t = 0 - self.vel.t
                self.p_center.y = float(10 + screen_height - self.rad)

        # finally round and set center coords
        self.center.x = int(round(self.p_center.x))
        self.center.y = int(round(self.p_center.y))

        # self.p_next_pos = self.next_positions[self.flag] # returns a tuple of two floats
        # self.center.x = int(round(self.p_next_pos[0]))
        # self.center.y = int(round(self.p_next_pos[1]))
        # self.flag += 1


class Ripple(object):
    """ripple object which emits from bodies on key press"""
    def __init__(self, pos, target, rad=0, alpha=100, max_r=200):
        self.target = target
        self.x, self.y = pos
        self.rad = rad
        self.alpha = alpha
        self.color = (150, 150, 150)
        self.max_r = max_r

    def pos(self):
        return self.x, self.y

    def update(self, model):
        self.rad = (40*self.rad + self.max_r) / 41
        self.alpha = self.alpha/1.1 - 1
        if self.alpha <= 0:
            model.ripples.remove(self)
        self.x, self.y = self.target.center.pos()

class Model(object):
    """ our Model class generates and edits body attributes, bodies are defined by points
    """

    # inits a custom number of bodies at semi-random positions inside screen
    def __init__(self, num_bodies=3, body_rad=10):
        self.ripples = [] 
        self.bodies = []
        self.body_centers = []
        global screen_size
        screen_width, screen_height = screen_size

        # self.body_centers = [
        #     Point(125, 125),
        #     Point(375, 125),
        #     Point(125, 375),
        #     Point(375, 375)]

        # creates list of center points for every body 
        while len(self.body_centers) < num_bodies:
            x = random.randint(0+body_rad, screen_width-body_rad)
            y = random.randint(0+body_rad, screen_height-body_rad)
            new_center = Point(x, y)
            if not self.too_close(new_center, self.body_centers, 2*body_rad):
                self.body_centers.append(new_center)

        # creates bodies at each center 
        for center in self.body_centers:
            self.bodies.append(Body(center.pos(), body_rad))

    def update(self):
        """ Updates all object to prep for draw
        """
        for body in self.bodies:
            body.update()
        for ripple in self.ripples:
            ripple.update(self)

    def too_close(self, new_point, points, distance):
        """ Checks to see if the new_point is too close to any points in points
        """
        if not points:
            return False
        for point in points:
            if math.hypot(
                    point.x - new_point.x,
                    point.y - new_point.y
                    ) < distance:
                return True
        return False


class PyGameWindowView(object):
    """ This puts everything on a scree
        So you can put your eyeballs on it
        and play, or whatever. 
    """
    def __init__(self, screen):
        self.screen = screen

    def draw(self, model):
        """ Draw background and all bodies
        """
        # paint background
        self.screen.fill((20, 20, 20))  # (255, 32, 103))


        # draw joining lines
        centers_list = [body.center.pos() for body in model.bodies]
        if len(model.bodies) > 1:
            pygame.gfxdraw.aapolygon(
                self.screen,
                centers_list,
                (100, 100, 100, 100)
                )

        # draw ripples
        ck = (127, 33, 33)
        for ripple in model.ripples:
            s = pygame.Surface((2*ripple.rad, 2*ripple.rad))
            s.fill(ck)
            s.set_colorkey(ck)
            s.set_alpha(ripple.alpha)
            pygame.draw.circle(
                s,
                ripple.color,
                (ripple.rad, ripple.rad),
                ripple.rad,
                )
            self.screen.blit(s, (ripple.x - ripple.rad, ripple.y - ripple.rad))


        # draw every body in bodies
        for body in model.bodies:
            circle_png = pygame.image.load('circle.png')
            self.screen.blit(circle_png, 
                            (body.center.x -5,
                            body.center.y -6 )
                            )
        # brings in our list of pos for each body center 
        # and then we draw bodies 
        pygame.display.update()


class PyGameAudio(object):
    """ This is where the audio is loaded
    """ 
    def __init__(self):
        # get paths for all .wavs in sounds flolder
        self.sound_paths = glob.glob('sounding/*.wav')
        print self.sound_paths  # SUB

    def play_sample_num(self, index):
        sound = pygame.mixer.Sound(self.sound_paths[index])
        sound.play()


class PyGameKeyboardController(object):
    """ Where loaded audio is mapped to keys 
    """ 
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
        elif event.key == pygame.K_f:
            audio_unit.play_sample_num(4)
        elif event.key == pygame.K_l:
            audio_unit.play_sample_num(5)
        elif event.key == pygame.K_k:
            audio_unit.play_sample_num(6)
            x = 250 
            y = 250 
            center_mass = Point(x,y) 
            for body in model.bodies:
                body.flag = 0
                body.next_positions = self.get_pos_list(body, center_mass) # pulls the list of coming postition for a node    
        elif event.key == pygame.K_j:
            audio_unit.play_sample_num(7)
            x = 250 
            y = 250 
            center_mass = Point(x,y) 
            for body in model.bodies:
            	body.flag = 0
                body.next_positions = self.get_pos_list(body, center_mass) # pulls the list of coming postition for a node
                
        #  space quits for speed in testing
        elif event.key == K_SPACE:
            global running
            running = False
        else:
            return

    def get_pos_list(self, body, center_mass):
        """ Calculates a list of future positions for a node
            given the event that B-key is pressed
        """ 

        pos_list = [] # empty list for all our postition for a node 

        # theta = math.atan(float(center_mass.y - body.center.y)/(body.center.x - center_mass.x))
        theta = random.uniform(0, 2*math.pi)
        if body.center.x < center_mass.x:
            theta += math.pi / 2
        print theta, body.center.pos()

        global frame_rate
        frame_list = range(0,frame_rate) # will be populated with our pos val for B-key event
        now_pos = body.center.pos() # pull the immediate location of the current node
        for frame in frame_list: 
            dist = self.pos_curve(frame,frame_rate) # get dist of movement for origial pos 
            dy = dist * math.sin(theta) # change in y pos
            dx = dist * math.cos(theta) # change in x pos 
            pos_list.append(tuple(map(sum, zip(now_pos, (dx, dy)))))
        # print pos_list
        return pos_list

    def pos_curve(self, frame, frame_rate):
        """ makes the bodies move nice...eventually 
        """
        dec = 0.137129
        frame_div = float(frame) / (frame_rate)
        dist = ( (math.log10((frame_div + dec)) + 1) / ((frame_div + dec)) - 1 ) * 500
        return dist

    def speed_random(self, model, velocity=10.0, spin=1.0):
        """ chooses a random body and gives it a particular speed
        """ 
        target = random.choice(model.bodies)
        target.vel.m = velocity
        target.acc.t = spin * random.choice((1, -1))
        model.ripples.append(Ripple(target.center.pos(),target))


if __name__ == '__main__':

    try:
        pygame.quit()
    except:
        pass

    pygame.init()
    frame_rate = 25
    screen_size = (500, 500)
    background = pygame.display.set_mode(screen_size)

    # loop = audio_unit.play_sample_num(9)
    # loop.play(-1)

    pygame.mixer.init(44100, -16, 2, 2048)

    # pygame.mixer.music.load("minor_mood.wav") 
    pygame.mixer.music.load("melancholy.wav") 
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0)
  
    model = Model(25, 5)
    audio_unit = PyGameAudio()
    view = PyGameWindowView(background)
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
