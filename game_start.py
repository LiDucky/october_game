import pygame, sys
from player import Player
from enemy import Enemy
import maps

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('October Game') # change for actual title later

# Window Size set
WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920
screen = pygame.display.set_mode(( WINDOW_WIDTH, WINDOW_HEIGHT ))

#initialize "Player" Class
player = Player()
enemies = []
for i in range(0, 3):
    enemies.append(Enemy())
gravity = 1
max_velocity = 13

camera_offset = [0, 0]

while True: # game loop
    camera_offset[0] += int(player.x-camera_offset[0]-WINDOW_WIDTH/2 + player.image.get_width()/2)
    camera_offset[1] += int(player.y-camera_offset[1]-WINDOW_HEIGHT/2 + player.image.get_height()/2)
    solid_tiles = []
    end_tiles = []
    
    for event in pygame.event.get():
        if event.type == QUIT: # user closes the window
            pygame.quit()
            sys.exit()

    screen.fill((0,0,0))
    y = 0
    for row in maps.map_two:
        x = 0
        for tile in row:
            if tile == 1:
                screen.blit(maps.tile_one, (x * maps.tile_size - camera_offset[0], y * maps.tile_size - camera_offset[1]))
            if tile == 2:
                screen.blit(maps.tile_two, (x * maps.tile_size - camera_offset[0], y * maps.tile_size - camera_offset[1]))
                end_tiles.append(pygame.Rect(x * maps.tile_size, y * maps.tile_size, maps.tile_size, maps.tile_size))
            if tile != 0 and tile != 2:
                solid_tiles.append(pygame.Rect(x * maps.tile_size, y * maps.tile_size, maps.tile_size, maps.tile_size))
            x += 1
        y += 1
    #Character Controls
    player.control(gravity, max_velocity)
    player.move(solid_tiles)
    for enemy in enemies:
        enemy.do_movement(gravity, max_velocity)
        enemy.move(solid_tiles)
        if player.hitbox.colliderect(enemy.hitbox):
            player.hurt(enemy.damage, screen)

    if not player.alive:
        text = pygame.font.Font(None, 20)
        text_surface = text.render("You died. :( press r to try again.", True, [255,255,255], [0,0,0])
        screen.blit(text_surface, (50, 50))
    if player.check_win(end_tiles):
        text = pygame.font.Font(None, 20)
        text_surface = text.render("You win!", True, [255,255,255], [0,0,0])
        screen.blit(text_surface, (50, 50))
    screen.blit(player.image, (player.x - camera_offset[0], player.y - camera_offset[1]))
    for enemy in enemies:
        screen.blit(enemy.image, (enemy.x - camera_offset[0], enemy.y - camera_offset[1]))
    player.draw_health(camera_offset, screen)
    
    # kill the player if they fall too far:
    # if player.y > WINDOW_HEIGHT:
    #     player.kill(screen)

    pygame.display.update()
    clock.tick(60) # run at 60fps
