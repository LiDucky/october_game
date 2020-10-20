import pygame

class Player():
    def __init__(self):

        self.image = pygame.image.load('Assets/Sprites/player.png')
        self.x = 300
        self. y = 300
        self.velocity_x = 5
        self.velocity_y = 0
        self.grounded = True
        # self.max_jumps = 1
    
    def respawn(self):
        self.x = 300
        self.y = 300

    def collision_test(self, rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, rect, movement, tiles):
        collision_types = {
            'top': False,
            'bottom': False,
            'right': False,
            'left': False
        }
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True    
        rect.y += movement[1]
        hit_list = collision_test(rect, tile)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[0] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types
