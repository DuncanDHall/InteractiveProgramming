import pygame
from pygame.locals import *
import time
import os
import random





class Model(object):
    def __init__(self):
        self.bodies = [ ] 
        self.body = Body((size[0]/2, size[1]/2), 50)

    def update(self):
        self.body.update()

class Body(object):
    def __init__(self,pos,rad,vel=(0.01, 0.01)):
        self.rad = rad
        self.pos = pos
        self.vel = vel
        self.acc = (0.0, 0.0)
    def update(self):
        self.pos = tuple(int(round(
            self.pos[i] + self.vel[i])) for i in range(2))
        self.vel = tuple(
            self.vel[i] + self.acc[i] for i in range(2))
        self.acc = tuple(
            self.acc[i] + random.uniform(-0.01, 0.01) for i in range(2))



class PyGameWindowView(object):
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def draw(self):
        self.screen.fill(pygame.Color(255, 32, 103))
        body = self.model.body

        pygame.draw.circle(
            self.screen,
            pygame.Color(0,0,0),
            body.pos,
            body.rad,
            3
        )

        pygame.display.update()

    def update(self):
        pass


class PyGameAudio(object):
    def __init__(self):
        pass

    def load_sounds(self):
        global cello_A2
        global cello_As2
        cello_A2 = pygame.mixer.Sound('sounds/cello_A2.wav')
        cello_As2 = pygame.mixer.Sound('sounds/cello_As2.wav')

    def play_sound_for_key(key):
        pass


class PyGameKeyboardController(object):
    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            print 'do something when left arrow is pressed'
        elif event.key == pygame.K_RIGHT:
            print 'right'
        elif event.key == pygame.K_a:
            cello_A2.play()
        elif event.key == pygame.K_s:
            cello_As2.play()
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
    audio_player = PyGameAudio()
    audio_player.load_sounds()

    size = (375, 467)
    screen = pygame.display.set_mode(size)

    model = Model()
    view = PyGameWindowView(model, screen)
    # controller = PyGameMouseController(model)

    controller = PyGameKeyboardController(model)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)

        model.update()
        view.draw()
        time.sleep(0.01)

    pygame.quit()
