import pygame, sys

from pygame.locals import *
pygame.init()

WINDOW_SIZE = (400,400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

while True: # game loop

    for event in pygame.event.get():
        if event.type == QUIT: # user closes the window
            pygame.quit()
            sys.exit()

    pygame.display.update()