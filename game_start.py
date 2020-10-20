import pygame, sys
from player import Player
import maps

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()
pygame.display.set_caption('October Game') # change for actual title later

# Window Size set
WINDOW_HEIGHT = 480
WINDOW_WIDTH = 720
screen = pygame.display.set_mode(( WINDOW_WIDTH, WINDOW_HEIGHT ))

#initialize "Player" Class
player = Player()
gravity = 2
max_velocity = 15
solid_tiles = []

while True: # game loop
    for event in pygame.event.get():
        if event.type == QUIT: # user closes the window
            pygame.quit()
            sys.exit()

    keys=pygame.key.get_pressed()
    if keys[pygame.K_r]: # Player model reset
        player.respawn()
    if keys[pygame.K_LEFT]:
        player.x -= player.velocity_x
    if keys[pygame.K_RIGHT]:
        player.x += player.velocity_x
    if player.grounded:
        player.velocity_y = 0
        if keys[pygame.K_UP]:
            player.velocity_y = -20
            player.grounded = False
    else:
        player.velocity_y += gravity
        if player.velocity_y > max_velocity:
            player.velocity_y = max_velocity

    player.y += player.velocity_y

    screen.fill((0,0,0))
    y = 0
    for row in maps.map_four:
        x = 0
        for tile in row:
            if tile == 1:
                screen.blit(maps.tile_one, (x * maps.tile_size, y * maps.tile_size))
            if tile != 0:
                solid_tiles.append(pygame.Rect(x * maps.tile_size, y * maps.tile_size, maps.tile_size, maps.tile_size))
            x += 1
        y += 1
    screen.blit(player.image, (player.x, player.y))
    
    pygame.display.update()
    clock.tick(60) # run at 60fps
    





