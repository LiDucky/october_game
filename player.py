import pygame
#colors:
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Player():
    def __init__(self):
        self.image = pygame.image.load('Assets/Sprites/player/idle.png')
        self.image.convert()
        self.max_airtime = 6
        self.airtime = 0
        self.x = 300
        self.y = 1000
        self.hitbox = pygame.Rect(self.x, self.y, 50, 60)
        self.velocity_x = 0
        self.velocity_y = 0
        self.alive = True
        self.health = 6
        self.max_health = 20
        # self.max_jumps = 1

    def hurt(self, damage, screen):
        self.health -= damage
        if self.health <= 0:
            self.kill(screen)
    
    def kill(self, screen):
        self.alive = False

    def collision_test(self, tiles):
        hit_list = []
        player_rect = self.image.get_rect(left=self.x, top=self.y)
        for tile in tiles:
            if player_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def draw_health(self, camera_offset, screen):
        pygame.draw.rect(screen, RED, (50, 50, self.max_health, 10))
        if self.health > 0:
            pygame.draw.rect(screen, GREEN, (50, 50, self.health, 10))


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
                self.airtime = 0
            elif self.velocity_y < 0:
                self.y = tile.bottom # collide on top side
                self.velocity_y = 0
        self.hitbox = pygame.Rect(self.x, self.y, 50, 60)
        return self.image.get_rect
    
    def check_win(self, tiles):
        player_rect = self.image.get_rect(left=self.x, top=self.y)
        for tile in tiles:
            if player_rect.colliderect(tile):
                return True

    def control(self, gravity, max_velocity):
        keys=pygame.key.get_pressed()
        self.velocity_x = 0
        if self.alive:
            if keys[pygame.K_LEFT]:
                self.velocity_x = -5
            if keys[pygame.K_RIGHT]:
                self.velocity_x = 5
            if self.airtime < self.max_airtime:
                self.airtime += 1
                if keys[pygame.K_UP]:
                    self.airtime = self.max_airtime
                    self.velocity_y = -25
        elif keys[pygame.K_r]: # Player repsawn
            self.alive = True
            self.x = 300
            self.y = 1000
        self.velocity_y += gravity
        if self.velocity_y > max_velocity:
            self.velocity_y = max_velocity