import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
from terrain import *


pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1365, 768
FPS = 60
PLAYER_VEL = 5
DAMAGE = 15
MAX_HEALTH = 100
HEALTHINCR = 35
DURATION = 5000

window = pygame.display.set_mode((WIDTH, HEIGHT))


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def flip_y(sprite):
    return pygame.transform.flip(sprite, False, True) 

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    ANIMATION_DELAY = 3
    GRAVITY=2
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        #self.SPRITES=load_sprite_sheets("MainCharacters",type, 32, 32, True)
        self.hp=100
        self.damage=15
        self.mask = None
        self.direction = "right"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 5
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, netherPlayer,dx, dy):
        if(self.rect.left>self.x_vel or self.direction=="right"):
            self.rect.x += dx
        self.rect.y += dy
        netherPlayer.rect.x=self.rect.x
        netherPlayer.rect.y=HEIGHT-self.rect.y-netherPlayer.height

    def make_hit(self):
        self.hit = True

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self,netherPlayer,fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(netherPlayer,self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        self.sprite_sheet = "idle"
        if self.hit:
            self.sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                self.sprite_sheet = "jump"
            elif self.jump_count == 2:
                self.sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            self.sprite_sheet = "fall"
        elif self.x_vel != 0:
            self.sprite_sheet = "run"

        sprite_sheet_name = self.sprite_sheet + "_" + self.direction
        self.sprites = self.SPRITES[sprite_sheet_name]
        self.sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(self.sprites)
        self.sprite = self.sprites[self.sprite_index]
        self.animation_count += 1
        self.update()

    def attack(self,enemy):
        if abs(self.rect.x-enemy.rect.x)<32 and abs(self.rect.y-enemy.rect.y)<32:
            enemy.hp-=self.damage

    def death(self):
        if self.hp<=0:
            GameOver(window)    

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
    

    
class NetherPlayer(pygame.sprite.Sprite):
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDudeReflect", 32, 32, True)
    def __init__(self,player,width,height):
        self.x=player.rect.x
        self.y=HEIGHT-player.rect.y-height
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.height=height
        self.width=width
    def animate(self,player):
        sprite_sheet_name = player.sprite_sheet + "_" + player.direction
        self.sprites = self.SPRITES[sprite_sheet_name]
        self.sprite=self.sprites[player.sprite_index]
    def draw(self, win, offset_x):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y-13))

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        self.rect=pygame.Rect(x,y,width,height)
        self.x_vel=3
        self.dx=0
        self.image_left=pygame.image.load("assets/zombieresize.png")
        self.image_right=pygame.image.load("assets/zombieresize_right.png")
        self.image=self.image_right
        self.direction="right"
        self.hp=40
        self.damage=25
    def walk(self,player,Flag):
        if self.dx==4 and self.image==self.image_right:
            self.image=self.image_left
        elif self.dx==0 and self.image==self.image_left:
            self.image=self.image_right
        if self.image==self.image_right:
            self.rect.x-=20
            self.dx+=1    
        else:
            self.rect.x+=20
            self.dx-=1
        self.attack(player,Flag)
    def draw(self,win,offset_x):
        self.rect=self.image.get_rect(topleft=(self.rect.x,self.rect.y))
        win.blit(self.image,(self.rect.x-offset_x,self.rect.y))
    '''def follow(self,player):
        if abs(self.rect.x-player.rect.x)<128 and abs(self.rect.y-player.rect.y)<128:
            if self.rect.x < player.rect.x:
                self.rect.x += PLAYER_VEL-2
            elif self.rect.x > player.rect.x:
                self.rect.x -= PLAYER_VEL-2
            if self.rect.y < player.rect.y:
                self.rect.y += PLAYER_VEL-2
            elif self.rect.y > player.rect.y:
                self.rect.y -= PLAYER_VEL-2'''
    def attack(self,player,Flag):
        if abs(self.rect.x-player.rect.x)<32 and abs(self.rect.y-player.rect.y)<32 and Flag:
            player.hp-=self.damage


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))
        win.blit(flip_y(self.image), (self.rect.x - offset_x, HEIGHT - self.rect.bottom))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

###edit 1 by Dhruv
class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, effect):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.duration = DURATION
        self.effect = effect
        

    def apply_effect(self, player):
        if self.effect == "health_pack":
            if player.hp > MAX_HEALTH - HEALTHINCR:
                player.hp = MAX_HEALTH
            else:
                player.hp+=HEALTHINCR    
        elif self.effect == "double_damage":
            player.damage *= 2
            pygame.time.set_timer(pygame.USEREVENT, self.duration)

    def end_effect(self, player):
        if self.effect == "double_damage":
            player.damage = player.damage //2  

    def draw(self, win, offset_x):
           win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Health_pack(Powerup):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size, "health_pack")
        self.image = pygame.image.load("assets/Powerups/Health_pack.png")
        self.image = pygame.transform.scale(self.image, (size, size))
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
 

class Double_damage(Powerup):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size, "double_damage")
        self.image = pygame.image.load("assets/Powerups/Double_damage.png")
        self.image = pygame.transform.scale(self.image, (size, size))
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
###end of edit 1 by D



def draw(window,bg_image, player, objects, netherPlayer, zombie, offset_x, powerups):
    bg_image=pygame.transform.scale(bg_image,(WIDTH,HEIGHT))
    window.blit(bg_image, (0,0))

    health=pygame.Rect(20,20,player.hp*2,32)
    pygame.draw.rect(window,(255,0,0),health,0)
    pygame.draw.rect(window,(0,0,0),health,2)

    for obj in objects:
        obj.draw(window, offset_x)
    for powerup in powerups:
        powerup.draw(window, offset_x)    
    zombie.draw(window,offset_x)
    player.draw(window, offset_x)
    netherPlayer.animate(player)
    netherPlayer.draw(window,offset_x)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, netherPlayer, objects, dx):
    player.move(netherPlayer,dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(netherPlayer,-dx, 0)
    player.update()
    return collided_object


def handle_move(player, netherPlayer, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, netherPlayer, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, netherPlayer, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()

##edit 2 by D

def makepowerup(blocksize, size):
    power_ups = [Health_pack(3*blocksize, HEIGHT//2-2*blocksize, size), Double_damage(6*blocksize, HEIGHT//2-2*blocksize, size), Double_damage(8*blocksize, HEIGHT//2-2*blocksize, size)]
    return power_ups

def collide_powerup(player, power_ups):
    collided_powerup = None
    for power_up in power_ups:
        if pygame.sprite.collide_mask(player, power_up):
            power_up.apply_effect(player)
            power_ups.remove(power_up)
            print(player.damage)
            print(player.hp)
            break
   

    return power_ups
# edit 2 by D            
    
def darken(event, object, coordinates):
    window.blit(object,coordinates)
    if event.type == pygame.MOUSEBUTTONDOWN:
        sub_button_sound = pygame.mixer.Sound('assets/Songs/sub_button.mp3')
        pygame.mixer.Channel(2).set_volume(1)
        pygame.mixer.Channel(2).play(sub_button_sound)
        return True
    return False
    
def GUI(window):
    font=pygame.font.SysFont("Palatino Linotype",32)
    selectChar=font.render("Select Character",False,(255,255,255))
    selectCharText=selectChar.get_rect(center=(130,200))
    wallpaper=pygame.image.load("assets/backgroundgui.jpg")
    wallpaper=pygame.transform.scale(wallpaper,(WIDTH,HEIGHT))
    
    about=pygame.image.load("assets/menu/Buttons/About.png")
    about_dark=pygame.image.load("assets/menu/Buttons/About_dark.png")
    play=pygame.image.load("assets/menu/Buttons/Play.png")
    play_dark=pygame.image.load("assets/menu/Buttons/Play_dark.png")

    mask_dude=pygame.image.load("assets/MainCharacters/MaskDude/jump.png")
    ninja_frog=pygame.image.load("assets/MainCharacters/NinjaFrog/jump.png")
    virtual_guy=pygame.image.load("assets/MainCharacters/VirtualGuy/jump.png")
    pink_man=pygame.image.load("assets/MainCharacters/PinkMan/jump.png")
    mask_dude_dark=flip_y(pygame.image.load("assets/MainCharacters/MaskDudeReflect/jump.png"))
    ninja_frog_dark=flip_y(pygame.image.load("assets/MainCharacters/NinjaFrogReflect/jump.png"))
    virtual_guy_dark=flip_y(pygame.image.load("assets/MainCharacters/VirtualGuyReflect/jump.png"))
    pink_man_dark=flip_y(pygame.image.load("assets/MainCharacters/PinkManReflect/jump.png"))

    preference=''
    about=pygame.transform.scale(about,(60,64))
    about_dark=pygame.transform.scale(about_dark,(60,64))
    play=pygame.transform.scale(play,(60,64))
    play_dark=pygame.transform.scale(play_dark,(60,64))

    logo=pygame.image.load("assets/NetherMirror.png")
    logo=pygame.transform.scale(logo,(400,274))

    window.blit(mask_dude,(120,230))
    window.blit(wallpaper,(0,0))
    window.blit(logo,(482,120))
    pygame.display.update()
    window.blit(mask_dude,(120,230))
    window.blit(ninja_frog,(120,270))
    window.blit(pink_man,(120,350))
    window.blit(virtual_guy,(120,310))
    window.blit(selectChar,selectCharText)
    done=False
    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            mousePos=pygame.mouse.get_pos()
            if 500<=mousePos[0]<=560 and 470<=mousePos[1]<=534:
                done=darken(event,about_dark,(500,470))
                if done:
                    About(window)
            else:
                window.blit(about,(500,470))
            if 805<=mousePos[0]<=865 and 470<=mousePos[1]<=534:
                done=darken(event,play_dark,(805,470))
            else:
                window.blit(play,(805,470))
            if 120<=mousePos[0]<=152 and 230<=mousePos[1]<=262:
                window.blit(mask_dude_dark,(120,230))
                if event.type==pygame.MOUSEBUTTONDOWN:
                    preference="MaskDude"
            else:
                window.blit(mask_dude,(120,230))
            if 120<=mousePos[0]<=152 and 270<=mousePos[1]<=302:
                window.blit(ninja_frog_dark,(120,270))
                if event.type==pygame.MOUSEBUTTONDOWN:
                    preference="NinjaFrog"
            else:
                window.blit(ninja_frog,(120,270))
            if 120<=mousePos[0]<=152 and 310<=mousePos[1]<=342:
                window.blit(virtual_guy_dark,(120,310))
                if event.type==pygame.MOUSEBUTTONDOWN:
                    preference="VirtualGuy"
            else:
                window.blit(virtual_guy,(120,310))
            if 120<=mousePos[0]<=152 and 350<=mousePos[1]<=392:
                window.blit(pink_man_dark,(120,350))
                if event.type==pygame.MOUSEBUTTONDOWN:
                    preference="PinkMan"
            else:
                window.blit(pink_man,(120,350))
        pygame.display.update()
    return preference

def About(window):
    font=pygame.font.SysFont("Palatino Linotype",32)

    credits=font.render('Nether Mirror by Dhruv Kothari and Nathan Mathew Verghese',False,(255,255,255))
    credits2=font.render('Additional credits to YT-techwithtim for learning resource, vecteezy.com for images',False,(255,255,255))
    credits3=font.render('and to design.ai for logo',False,(255,255,255))
    creditText=credits.get_rect(center=(682,384))
    creditText2=credits2.get_rect(center=(682,420))
    creditText3=credits3.get_rect(center=(682,456))

    window.blit(credits,creditText)
    window.blit(credits2,creditText2)
    window.blit(credits3,creditText3)

    wallpaper=pygame.image.load("assets/backgroundgui.jpg")
    wallpaper=pygame.transform.scale(wallpaper,(WIDTH,HEIGHT))
    back=pygame.image.load("assets/menu/Buttons/Back.png")
    back_dark=pygame.image.load("assets/menu/Buttons/Back_dark.png")
    back=pygame.transform.scale(back,(60,64))
    back_dark=pygame.transform.scale(back_dark,(60,64))
    window.blit(wallpaper,(0,0))
    window.blit(back,(500,570))
    pygame.display.update()
    done=False
    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            mousePos=pygame.mouse.get_pos()
            if 500<=mousePos[0]<=560 and 570<=mousePos[1]<=634:
                done=darken(event,back_dark,(500,570))
                if done:
                    GUI(window)
            else:
                window.blit(back,(500,570))
        window.blit(credits,creditText)
        window.blit(credits2,creditText2)
        window.blit(credits3,creditText3)
        pygame.display.update()
        
def GameOver(window):
    font=pygame.font.SysFont("Palatino Linotype",32)
    text=font.render('Game Over',False,(255,255,255))
    wallpaper=pygame.image.load("assets/backgroundgui.jpg")
    wallpaper=pygame.transform.scale(wallpaper,(WIDTH,HEIGHT))
    window.blit(wallpaper,(0,0))
    textbox=text.get_rect(center=(682,284))
    window.blit(text,textbox)
    re=pygame.image.load("assets/menu/Buttons/Restart.png")
    re_dark=pygame.image.load("assets/menu/Buttons/Restart_dark.png")
    done=False
    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            mousePos=pygame.mouse.get_pos()
            if 682<=mousePos[0]<=742 and 570<=mousePos[1]<=634:
                done=darken(event,re_dark,(682,570))
            else:
                window.blit(re,(682,570))



def main(window):
    Flag=False
    clock = pygame.time.Clock()
    bg_image=pygame.image.load("assets/background/background.png")
    type=GUI(window)

    block_size = 64
    zombie=Enemy(block_size/2+500,HEIGHT//2-block_size,32,52)
    player = Player(block_size/2, HEIGHT//2-block_size, 50, 50)
    netherPlayer=NetherPlayer(player,50,50)
    fire = Fire(block_size/2, HEIGHT//2 - block_size, 32, 32)
    fire.on()
    floor = [Block(i * block_size, (HEIGHT//2 - block_size), block_size)
             for i in range(-block_size, (WIDTH * 2) // block_size)]
    objects=[*floor]
    objects.extend(makemap(objects,block_size))

    zombies = []
    power_ups = makepowerup(block_size, block_size)

    #objects = makemap(objects, block_size)

    offset_x = 0
    scroll_area_width = 2*block_size

    run = True
    while run:
        clock.tick(FPS)
        Flag=not Flag
        #for i in range(2,HEIGHT//block_size+1):
         #   objects.append(Block(-block_size + offset_x, HEIGHT-block_size*i, block_size))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif(event.type == pygame.USEREVENT):   #changes made by dhruv
                for powerup in power_ups:
                    powerup.end_effect(player)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(netherPlayer,FPS)
        fire.loop()
        zombie.walk(player,Flag)
        handle_move(player, netherPlayer, objects)
        #edit 3
        power_ups = collide_powerup(player, power_ups)
        pygame.display.update()
        #edit 3 end
        draw(window,bg_image, player, objects, netherPlayer,zombie, offset_x, power_ups)
        #bg_image=pygame.transform.scale(bg_image,(WIDTH,HEIGHT))
        #window.blit(bg_image, (0,0))

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0):
              # or  ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
