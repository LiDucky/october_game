import pygame
import random

# define colors
GREEN = (0, 255, 0)

class Enemy():
    def __init__(self):
        self.image = pygame.image.load('Assets/Sprites/player.png') # TODO: change to enemy image
        self.image.convert()
        self.x = 100#random.randrange(1920 - self.image.get_width()) #passs in window width
        self.y = 100#random.randrange(-100, -40)
        self.velocity_x = random.randrange(-3, 3)
        self.velocity_y = random.randrange(1, 8) # change so they can't drift about randomly vertically
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
        return self.image.get_rect

# # I think this would go in game_start
# all_sprites = pygame.sprite.Group()
# enemies = pygame.sprite.Group()
# player = Player()
# all_sprites.add(player)
# for i in range(8):
#     e = enemy()
#     all_sprites.add(e)
#     enemies.add(e)