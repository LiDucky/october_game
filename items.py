import pygame

class Item():
    def __init__(self, position_x, position_y, width=64, height=64):
        self.image = pygame.image.load("Assets\Sprites\coin.png")
        self.image.convert()
        self.x = position_x
        self.y = position_y
        self.hitbox = pygame.Rect(self.x, self.y,width, height)
        self.active = True
        # self.move_count = 0 # for some basic animation
    
    def player_contact(self, player):   
        if self.hitbox.colliderect(player):
            self.active = False # change later so it's whatever the item does on pickup
        
