import pygame, sys, maps, random
from player import Player
from enemy import Enemy
from items import Item
from particle import Particle
from pygame.locals import *
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('October Game') # change for actual title later
clock = pygame.time.Clock()

# Window Size set
WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920
screen = pygame.display.set_mode(( WINDOW_WIDTH, WINDOW_HEIGHT))

# Initialize "Player" Class
player = Player()
victory = False

# World Settings
camera_offset = [0, 0]
gravity = 1
max_velocity_x = 10
max_velocity_y = 15
particles = []
attack_interval = 0
isRight = True # TEMP Checks player Facing; can be later added to player class
score = 0
font = pygame.font.Font('freesansbold.ttf', 25)

# Show Score
def show_score(x, y):
    score = player.kills * 100 + player.coins_collected * 10
    screen.blit(font.render("Score: " + str(score), True, (255,255,255)), (x, y))

# Enemy Spawn
def spawn_enemy():
    enemies = []
    for i in range(0, 3):
        enemies.append(Enemy())
    return enemies
enemies = spawn_enemy()

# Item Spawn
def spawn_item():
    items = [Item(1280,750, "coin"),Item(1085, 270, "health"),Item(1580, 1050, "health"),Item(2175, 1230, "coin"),Item(380, 270, "coin")]
    return items
items = spawn_item()

# FPS counter
def show_fps():
    screen.blit(font.render(str(int(clock.get_fps())), True, (255,255,255)), (WINDOW_WIDTH - 100, 100))

# Main Menu
click = False
def main_menu():
    def create_font(t, s=72, c=(255, 255, 255), b=False, i=False):
        font = pygame.font.Font('freesansbold.ttf', s, bold=b, italic=i)
        text = font.render(t, True, c)
        return text
    
    while True:

        mouse = pygame.mouse.get_pos()
        start_game = create_font('START GAME')
        button_1 = screen.blit(start_game, (560, 350))
        start_game = create_font('START GAME')
        button_1 = screen.blit(start_game, (560, 350))
        start_game = create_font('START GAME')
        button_1 = screen.blit(start_game, (560, 350))

while True: # Main Game Loop
    # Camera Controls
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
    
    # Particles
    if pygame.mouse.get_pressed()[0]:
        particles.append(Particle(pygame.mouse.get_pos()[0] - camera_offset[0], pygame.mouse.get_pos()[1] - camera_offset[1]))

    # Generate Tiles
    solid_tiles = []
    end_tiles = []

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
            if tile == 3:
                screen.blit(maps.tile_three, (x * maps.tile_size - camera_offset[0], y * maps.tile_size - camera_offset[1]))
            if tile != 0 and tile != 2:
                solid_tiles.append(pygame.Rect(x * maps.tile_size, y * maps.tile_size, maps.tile_size, maps.tile_size))
            x += 1
        y += 1

    # Character Controls
    player.last_hit += 1
    player.control(gravity, max_velocity_x, max_velocity_y)
    player.move(solid_tiles)
    player.draw_health(camera_offset, screen)

    # Attack Logic
    attack = [] # Attack List
    if attack_interval > 0: # Attack interval timer
        attack_interval -= 1
    keys=pygame.key.get_pressed()
    if keys[pygame.K_SPACE]: # Attack Command
        if attack_interval == 0:
            if player.isRight:
                attack1 = pygame.Rect(player.x + 50, player.y, player.image.get_width(), player.image.get_height())
                pygame.draw.rect(screen,(255,0,0), (player.x + 50-camera_offset[0], player.y-camera_offset[1], player.image.get_width(), player.image.get_height())) # Insert attack animation here
                attack.append(attack1)
            else:
                attack1 = pygame.Rect(player.x - 50, player.y, player.image.get_width(), player.image.get_height())
                pygame.draw.rect(screen,(255,0,0), (player.x - 50-camera_offset[0], player.y-camera_offset[1], player.image.get_width(), player.image.get_height())) # Insert attack animation here
                attack.append(attack1)
            attack_interval = 15 # Sets max attack delay

    # Enemy Controls
    for enemy in enemies:
        enemy.do_movement(player, gravity, max_velocity_y)
        enemy.move(solid_tiles)
        screen.blit(pygame.transform.flip(enemy.image, enemy.flip, False), (enemy.x - camera_offset[0], enemy.y - camera_offset[1]))
        if player.hitbox.colliderect(enemy.hitbox):
            player.hurt(enemy, screen)
        if len(attack) > 0: # Attack Check
            if enemy.hitbox.colliderect(attack[0]):
                enemy.damage_check(player, items, enemies)

    # Item Controls
    for item in items:
        item.functions(screen, camera_offset, player)

    # Win / Lose Conditions
    if not player.alive and victory == False:
        text_surface = font.render("Game Over! :( Press 'R' to Play Again.", True, [255,255,255], [0,0,0])
        screen.blit(text_surface, (750, 50))
        if keys[pygame.K_r]: # Player repsawn
            score = 0
            victory = False
            player.health = player.max_health
            player.alive = True
            player.x = 300
            player.y = 1000
            enemies = spawn_enemy()
            items = spawn_item()
    if player.check_win(end_tiles):
        if len(enemies) > 0:
            text_surface = font.render("Defeat All Enemies!", True, [255,255,255], [0,0,0])
            screen.blit(text_surface, (850, 50))
        else:
            victory = True
            player.kill()
    if victory:
        text_surface = font.render("You win! Press 'R' to Play Again.", True, [255,255,255], [0,0,0])
        screen.blit(text_surface, (800, 50))
        if keys[pygame.K_r]: # Player repsawn
            score = 0
            victory = False
            player.health = player.max_health
            player.alive = True
            player.x = 300
            player.y = 1000
            enemies = spawn_enemy()
            items = spawn_item()


    # Player Blit
    screen.blit(pygame.transform.flip(player.image, player.flip, False), (player.x - camera_offset[0], player.y - camera_offset[1]))
    
    
    # Particle Controls
    for i in range(len(particles)-1, -1, -1):
        particles[i].x += particles[i].velocity_x
        particles[i].y += particles[i].velocity_y
        pygame.draw.circle(screen, particles[i].color, (int(particles[i].x) - camera_offset[0], int(particles[i].y) - camera_offset[1]), int(particles[i].radius))
        particles[i].radius -= .1
        if particles[i].radius <= 0:
            particles.pop(i)

    # Exit the Game
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            sys.exit()

    
    show_score(500, 100)
    show_fps()
    pygame.display.update()
    clock.tick(60) # run at 60fps
