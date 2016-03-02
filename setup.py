import pygame
from pygame.locals import *
import time


class Model(object):
    pass


class PyGameWindowView(object):
    def __init__(self):
        pass

    def update(self):
        pass


class PyGameKeyboardController(object):
    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            print 'do something when left arrow is pressed'
        else:
            return


if __name__ == '__main__':
    pygame.init()

    size = (375, 667)
    screen = pygame.display.set_mode(size)

    model = Model()
    view = PyGameWindowView(model, screen)
    # controller = PyGameMouseController(model)

    controller = PyGameKeyboardController(model)

    running = True

    while running:
        for event in pygamge.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)

        moedel.update()
        view.draw()
        time.sleep(0.001)

    pygame.quit()