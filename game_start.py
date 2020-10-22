import pygame, sys
from player import Player
from enemy import Enemy
from items import Item
from particle import Particle
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
max_velocity_x = 10
max_velocity_y = 15

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 25)

particles = []

def show_score(x, y):
    score = player.kills * 100 + player.coins_collected * 10
    screen.blit(font.render("Score: " + str(score), True, (255,255,255)), (x, y))

# Attack Test
attack_interval = 0
isRight = True # TEMP Checks player Facing; can be later added to player class

camera_offset = [0, 0]

while True: # game loop
    camera_offset[0] += int(player.x-camera_offset[0]-WINDOW_WIDTH/2 + player.image.get_width()/2)
    camera_offset[1] += int(player.y-camera_offset[1]-WINDOW_HEIGHT/2 + player.image.get_height()/2)
    if camera_offset[0] < 0:
        camera_offset[0] = 0
    if camera_offset[1] < 0:
        camera_offset[1] = 0
    if camera_offset[0] > len(maps.map_five[0]) * maps.tile_size - WINDOW_WIDTH:
        camera_offset[0] = len(maps.map_five[0]) * maps.tile_size - WINDOW_WIDTH
    if camera_offset[1] > len(maps.map_five) * maps.tile_size - WINDOW_HEIGHT:
        camera_offset[1] = len(maps.map_five) * maps.tile_size - WINDOW_HEIGHT
    solid_tiles = []
    end_tiles = []

    if pygame.mouse.get_pressed()[0]:
        particles.append(Particle(pygame.mouse.get_pos()))

    for event in pygame.event.get():
        if event.type == QUIT: # user closes the window
            pygame.quit()
            sys.exit()

    screen.fill((0,0,0))
    y = 0
    for row in maps.map_five:
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
    player.last_hit += 1
    player.control(gravity, max_velocity_x, max_velocity_y)
    player.move(solid_tiles)

    # Attack Test
    attack = [] # Attack List
    if attack_interval > 0: # Attack interval timer
        attack_interval -= 1
    keys=pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        isRight = True # TEMP Checks player Facing; can be later added to player class
    if keys[pygame.K_LEFT]:
        isRight = False # TEMP Checks player Facing; can be later added to player class
    if keys[pygame.K_SPACE]: # Attack Command
        if attack_interval == 0:
            if isRight:
                attack1 = pygame.Rect(player.x + 50, player.y, player.image.get_width(), player.image.get_height())
                pygame.draw.rect(screen,(255,0,0), (player.x + 50-camera_offset[0], player.y-camera_offset[1], player.image.get_width(), player.image.get_height())) # Insert attack animation here
                attack.append(attack1)
            else:
                attack1 = pygame.Rect(player.x - 50, player.y, player.image.get_width(), player.image.get_height())
                pygame.draw.rect(screen,(255,0,0), (player.x - 50-camera_offset[0], player.y-camera_offset[1], player.image.get_width(), player.image.get_height())) # Insert attack animation here
                attack.append(attack1)
            attack_interval = 50 # Sets max attack delay

    for enemy in enemies:
        enemy.do_movement(player, gravity, max_velocity_y)
        enemy.move(solid_tiles)
        if player.hitbox.colliderect(enemy.hitbox):
            player.hurt(enemy, screen)
        if len(attack) > 0: # Attack Check
            if enemy.hitbox.colliderect(attack[0]):
                enemy.hurt(player, enemies)
                # enemies.pop(enemies.index(enemy)) # Delete hit enemy

    for i in range(len(particles)-1, -1, -1):
        particles[i].x += particles[i].velocity_x
        particles[i].y += particles[i].velocity_y
        pygame.draw.circle(screen, particles[i].color, (int(particles[i].x), int(particles[i].y)), int(particles[i].radius))
        particles[i].radius -= .1
        if particles[i].radius <= 0:
            particles.pop(i)

    show_score(500, 100)
    if not player.alive:
        text = pygame.font.Font(None, 20)
        text_surface = text.render("You died. :( press r to try again.", True, [255,255,255], [0,0,0])
        screen.blit(text_surface, (50, 50))
    if player.check_win(end_tiles):
        text = pygame.font.Font(None, 20)
        text_surface = text.render("You win!", True, [255,255,255], [0,0,0])
        screen.blit(text_surface, (50, 50))
    screen.blit(pygame.transform.flip(player.image, player.flip, False), (player.x - camera_offset[0], player.y - camera_offset[1]))
    for enemy in enemies:
        screen.blit(enemy.image, (enemy.x - camera_offset[0], enemy.y - camera_offset[1]))
    player.draw_health(camera_offset, screen)
    
    # kill the player if they fall too far:
    # if player.y > WINDOW_HEIGHT:
    #     player.kill(screen)


    pygame.display.update()
    clock.tick(60) # run at 60fps
