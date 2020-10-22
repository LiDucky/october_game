import pygame
import random

# define colors
GREEN = (0, 255, 0)
global animation_frames
animation_frames = {}

class Enemy():
    def __init__(self):
        self.image = pygame.image.load('Assets/Sprites/enemy/walk/walk0.png')
        self.image.convert()
        self.x = random.randrange(1920 - self.image.get_width()) #pass in window width
        self.y = 300 #random.randrange(-100, -40)
        self.hitbox = pygame.Rect(self.x, self.y, 50, 60)
        self.has_jumped = True;
        self.damage = 1
        self.max_velocity_x = 8
        self.velocity_x = 0 # in the future add ai so it'll jump
        self.velocity_y = 0 # in the future add ai so it'll jump
        self.health = 6 # change later and add function to modify

        self.state = "idle"
        self.frame = 0
        self.flip = False
        self.animation_database = {}
        self.animation_database["walk"] = self.load_animation("Assets/Sprites/player/walk", [7,7])

    def drop_stuff(self):
        random_num = random.randrange(1,100)
        if random_num >=50:
            item_drop = Item(self.x, self.y, "coin")
            # items.append(item_drop) #need to append to the items list from game_start

    def hurt(self, player, all_enemies):
        self.health -= player.damage
        if (player.x + player.image.get_width()/2) > (self.x + self.image.get_width()/2):
            self.velocity_x = -20
        else:
            self.velocity_x = 20
        if self.health <= 0:
            player.kills += 1
            all_enemies.remove(self)

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
                self.has_jumped = False
                self.y = tile.top - int(self.image.get_height()) # collide on bottom side
                self.velocity_y = 0
            elif self.velocity_y < 0:
                self.y = tile.bottom # collide on top side
                self.velocity_y = 0
        self.hitbox = pygame.Rect(self.x, self.y, 50, 60)
        return self.image.get_rect

    def do_movement(self, player, gravity, max_velocity_y):
        if player.x < self.x:
            if self.velocity_x > -self.max_velocity_x:
                self.velocity_x -= 2
            if self.velocity_x <= -self.max_velocity_x:
                self.velocity_x = -self.max_velocity_x
            self.state = self.change_state(self.state, "walk")
            self.flip = True
        elif player.x > self.x:
            if self.velocity_x < self.max_velocity_x:
                self.velocity_x += 2
            if self.velocity_x >= self.max_velocity_x:
                self.velocity_x = self.max_velocity_x
            self.state = self.change_state(self.state, "walk")
            self.flip = False
        if player.y < self.y:
            # do jump?
            if not self.has_jumped:
                self.has_jumped = True
                self.velocity_y = -20 # add ground condition, flying enemies are a no-go.
        self.velocity_y += gravity
        if self.velocity_y > max_velocity_y:
            self.velocity_y = max_velocity_y
    
    def change_state(self, current_state, state):
        if current_state != state:
            current_state = state
            self.frame = 0
        return current_state

    def load_animation(self, path, frame_durations):
        global animation_frames
        animation_name = path.split('/')[-1]
        animation_frame_data = []
        n = 0
        for frame in frame_durations:
            animation_frame_id = animation_name + str(n)
            img_loc = path + "/" + animation_frame_id + ".png"
            animation_image = pygame.image.load(img_loc)
            animation_frames[animation_frame_id] = animation_image.copy()
            for i in range(frame):
                animation_frame_data.append(animation_frame_id)
            n += 1
        return animation_frame_data

