import pygame, sys
from player import Player
import maps

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()
pygame.display.set_caption('October Game') # change for actual title later

# Window Size set
WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920
screen = pygame.display.set_mode(( WINDOW_WIDTH, WINDOW_HEIGHT ))

#initialize "Player" Class
player = Player()
gravity = 2
max_velocity = 15

while True: # game loop
    solid_tiles = []
    end_tiles = []
    
    for event in pygame.event.get():
        if event.type == QUIT: # user closes the window
            pygame.quit()
            sys.exit()

    #Character Controls
    player.control(gravity, max_velocity)


    screen.fill((0,0,0))
    y = 0
    for row in maps.map_two:
        x = 0
        for tile in row:
            if tile == 1:
                screen.blit(maps.tile_one, (x * maps.tile_size, y * maps.tile_size))
            if tile == 2:
                screen.blit(maps.tile_two, (x * maps.tile_size, y * maps.tile_size))
                end_tiles.append(pygame.Rect(x * maps.tile_size, y * maps.tile_size, maps.tile_size, maps.tile_size))
            if tile != 0 and tile != 2:
                solid_tiles.append(pygame.Rect(x * maps.tile_size, y * maps.tile_size, maps.tile_size, maps.tile_size))
            x += 1
        y += 1
    
    player.move(solid_tiles)
    if player.check_win(end_tiles):
        text = pygame.font.Font(None, 20)
        text_surface = text.render("You win!", True, [255,255,255], [0,0,0])
        screen.blit(text_surface, (50, 50))
    screen.blit(player.image, (player.x, player.y))
    
    if player.y > WINDOW_HEIGHT:
        # add text for player death
        text = pygame.font.Font(None, 20)
        text_surface = text.render("You died. :( press r to try again.", True, [255,255,255], [0,0,0])
        screen.blit(text_surface, (50, 50))
        if keys[pygame.K_r]: # Player model reset
            player.respawn()

    pygame.display.update()
    clock.tick(60) # run at 60fps
