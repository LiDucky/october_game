import pygame
import random

# define colors
GREEN = (0, 255, 0)

class Enemy():
    def __init__(self):
        self.image = pygame.image.load('Assets/Sprites/player.png') # TODO: change to enemy image
        self.image.convert()
        self.x = random.randrange(1920 - self.image.get_width()) #pass in window width
        self.y = 300 #random.randrange(-100, -40)
        self.hitbox = pygame.Rect(self.x, self.y, 50, 60)
        self.damage = 1
        self.velocity_x = 0 # in the future add ai so it'll jump
        self.velocity_y = 0 # in the future add ai so it'll jump
        self.health = 6 # change later and add function to modify

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    def collision_test(self, tiles):
        hit_list = []
        player_rect = self.image.get_rect(left=self.x, top=self.y)
        for tile in tiles:
            if player_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, tiles):
        self.x += self.velocity_x
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.velocity_x > 0:
                self.x = tile.left - int(self.image.get_width()) # collide on right side
            elif self.velocity_x < 0:
                self.x = tile.right # collide on left side
        self.y += self.velocity_y
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.velocity_y > 0:
                self.y = tile.top - int(self.image.get_height()) # collide on bottom side
                self.velocity_y = 0
            elif self.velocity_y < 0:
                self.y = tile.bottom # collide on top side
                self.velocity_y = 0
        self.hitbox = pygame.Rect(self.x, self.y, 50, 60)
        return self.image.get_rect

    def do_movement(self, gravity, max_velocity):
        # this will end up being tied to our ai
        self.velocity_x = -5
        self.velocity_y += gravity
        if self.velocity_y > max_velocity:
            self.velocity_y = max_velocity

# # I think this would go in game_start
# all_sprites = pygame.sprite.Group()
# enemies = pygame.sprite.Group()
# player = Player()
# all_sprites.add(player)
# for i in range(8):
#     e = enemy()
#     all_sprites.add(e)
#     enemies.add(e)