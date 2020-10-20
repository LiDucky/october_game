import pygame

class Player():
    def __init__(self):

        self.image = pygame.image.load('Assets/Sprites/player.png')
        self.image.convert()
        self.x = 300
        self.y = 300
        self.velocity_x = 0
        self.velocity_y = 0
        self.grounded = False
        # self.max_jumps = 1
    
    def respawn(self):
        self.x = 300
        self.y = 300

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
                self.veolcity_y = 0
                self.grounded = True
            elif self.velocity_y < 0:
                self.y = tile.bottom # collide on top side
                self.velocity_y = 0
        return self.image.get_rect
