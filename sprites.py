import pygame
from configuration import *
import math
import random 

class SpriteSheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert()
    
    def getSprite(self,x,y,width,height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet,(0,0),(x,y,width,height))
        sprite.set_colorkey((0,0,0))
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer=playerLayer
        self.groups=self.game.allSprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*tileSize
        self.y=y*tileSize
        self.width=tileSize
        self.height=tileSize

        self.xChange=0
        self.yChange=0

        self.facing='down'
        self.animationLoop=1

        self.image=self.game.characterSpriteSheet.getSprite(3,2,self.width,self.height)
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

    def update(self):
        self.movement()
        self.animate()
        self.collideEnemy()
        self.rect.x+=self.xChange
        self.collideBlock('x')
        self.rect.y+=self.yChange
        self.collideBlock('y')
        self.xChange=0
        self.yChange=0

    def movement(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.allSprites:
                sprite.rect.x +=playerSpeed
            self.xChange-=playerSpeed
            self.facing='left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.allSprites:
                sprite.rect.x -=playerSpeed
            self.xChange+=playerSpeed
            self.facing='right'
        if keys[pygame.K_UP]:
            for sprite in self.game.allSprites:
                sprite.rect.y +=playerSpeed
            self.yChange-=playerSpeed
            self.facing='up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.allSprites:
                sprite.rect.y -=playerSpeed
            self.yChange+=playerSpeed
            self.facing='down'
    
    def collideBlock(self,direction):
        if direction=="x":
            hits=pygame.sprite.spritecollide(self,self.game.blocks,False)
            if hits:
                if self.xChange>0:
                    self.rect.x=hits[0].rect.left-self.rect.width
                    for sprite in self.game.allSprites:
                        sprite.rect.x+=playerSpeed
                elif self.xChange<0:
                    self.rect.x=hits[0].rect.right
                    for sprite in self.game.allSprites:
                        sprite.rect.x-=playerSpeed

        if direction=="y":
            hits=pygame.sprite.spritecollide(self,self.game.blocks,False)
            if hits:
                if self.yChange>0:
                    self.rect.y=hits[0].rect.top-self.rect.height
                    for sprite in self.game.allSprites:
                        sprite.rect.y+=playerSpeed
                elif self.yChange<0:
                    self.rect.y=hits[0].rect.bottom
                    for sprite in self.game.allSprites:
                        sprite.rect.y-=playerSpeed

    def collideEnemy(self):
        hits=pygame.sprite.spritecollide(self,self.game.enemies,False)
        if hits:
            self.kill()
            self.game.playing=False

    def animate(self):
        downAnimation = [self.game.characterSpriteSheet.getSprite(3, 2, self.width, self.height),
                        self.game.characterSpriteSheet.getSprite(35, 2, self.width, self.height),
                        self.game.characterSpriteSheet.getSprite(68, 2, self.width, self.height)]

        upAnimation = [self.game.characterSpriteSheet.getSprite(3, 34, self.width, self.height),
                      self.game.characterSpriteSheet.getSprite(35, 34, self.width, self.height),
                      self.game.characterSpriteSheet.getSprite(68, 34, self.width, self.height)]

        leftAnimation = [self.game.characterSpriteSheet.getSprite(3, 98, self.width, self.height),
                        self.game.characterSpriteSheet.getSprite(35, 98, self.width, self.height),
                        self.game.characterSpriteSheet.getSprite(68, 98, self.width, self.height)]

        rightAnimation = [self.game.characterSpriteSheet.getSprite(3, 66, self.width, self.height),
                         self.game.characterSpriteSheet.getSprite(35, 66, self.width, self.height),
                         self.game.characterSpriteSheet.getSprite(68, 66, self.width, self.height)]
        
        if self.facing=="down":
            if self.yChange==0:
                self.image = downAnimation[0]
            else:
                self.image=downAnimation[math.floor(self.animationLoop)]
                self.animationLoop+=0.1
                if self.animationLoop>=3:
                    self.animationLoop=1
        if self.facing=="up":
            if self.yChange==0:
                self.image = upAnimation[0]
            else:
                self.image=upAnimation[math.floor(self.animationLoop)]
                self.animationLoop+=0.1
                if self.animationLoop>=3:
                    self.animationLoop=1
        if self.facing=="left":
            if self.xChange==0:
                self.image = leftAnimation[0]
            else:
                self.image=leftAnimation[math.floor(self.animationLoop)]
                self.animationLoop+=0.1
                if self.animationLoop>=3:
                    self.animationLoop=1
        if self.facing=="right":
            if self.xChange==0:
                self.image = rightAnimation[0]
            else:
                self.image=rightAnimation[math.floor(self.animationLoop)]
                self.animationLoop+=0.1
                if self.animationLoop>=3:
                    self.animationLoop=1

class Enemy(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer=enemyLayer
        self.groups=self.game.allSprites,self.game.enemies
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*tileSize
        self.y=y*tileSize
        self.width=tileSize
        self.height=tileSize

        self.xChange=0
        self.yChange=0
        
        self.facing=random.choice(['left','right'])
        self.animationLoop=1
        self.movementLoop=0
        self.maxTravel=random.randint(7,30)

        self.image=self.game.enemySpriteSheet.getSprite(3,2,self.width,self.height)
        self.image.set_colorkey((0,0,0))
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

    def update(self):
        self.movement()
        self.animate()
        self.rect.x+=self.xChange
        self.rect.y+=self.yChange

        self.xChange=0
        self.yChange=0
    
    def movement(self):
        if self.facing=='left':
            self.xChange-=enemySpeed
            self.movementLoop-=1
            if self.movementLoop<=-self.maxTravel:
                self.facing='right'
        if self.facing=='right':
            self.xChange+=enemySpeed
            self.movementLoop+=1
            if self.movementLoop>=self.maxTravel:
                self.facing='left'
    
    def animate(self):
        leftAnimation = [self.game.enemySpriteSheet.getSprite(3, 98, self.width, self.height),
                        self.game.enemySpriteSheet.getSprite(35, 98, self.width, self.height),
                        self.game.enemySpriteSheet.getSprite(68, 98, self.width, self.height)]

        rightAnimation = [self.game.enemySpriteSheet.getSprite(3, 66, self.width, self.height),
                         self.game.enemySpriteSheet.getSprite(35, 66, self.width, self.height),
                         self.game.enemySpriteSheet.getSprite(68, 66, self.width, self.height)]
        
        if self.facing=="left":
            if self.xChange==0:
                self.image = leftAnimation[0]
            else:
                self.image=leftAnimation[math.floor(self.animationLoop)]
                self.animationLoop+=0.1
                if self.animationLoop>=3:
                    self.animationLoop=1
        if self.facing=="right":
            if self.xChange==0:
                self.image = rightAnimation[0]
            else:
                self.image=rightAnimation[math.floor(self.animationLoop)]
                self.animationLoop+=0.1
                if self.animationLoop>=3:
                    self.animationLoop=1

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game=game
        self._layer=blockLayer
        self.groups=self.game.allSprites,self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*tileSize
        self.y=y*tileSize
        self.width=tileSize
        self.height=tileSize

        self.image=self.game.terrainSpriteSheet.getSprite(960,448,self.width,self.height)
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer=groundLayer
        self.groups=self.game.allSprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*tileSize
        self.y=y*tileSize
        self.width=tileSize
        self.height=tileSize

        self.image=self.game.terrainSpriteSheet.getSprite(64,352,self.width,self.height)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Button:
    def __init__(self,x,y,width,height,fgColor,bgColor,content,fontSize):
        self.font=pygame.font.SysFont('Avenir',fontSize)
        self.content=content

        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.fgColor=fgColor
        self.bgColor=bgColor

        self.image=pygame.Surface((self.width,self.height))
        self.image.fill(self.bgColor)
        self.rect=self.image.get_rect()

        self.rect.x=self.x
        self.rect.y=self.y

        self.text=self.font.render(self.content,True,self.fgColor)
        self.textRect = self.text.get_rect(center=(self.width/2,self.height/2))
        self.image.blit(self.text,self.textRect)

    def isPressed(self,pos,pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    
class Attack(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer=playerLayer
        self.groups=self.game.allSprites,self.game.attacks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x=x
        self.y=y
        self.width=tileSize
        self.height=tileSize
        
        self.animationLoop=0
        
        self.image=self.game.attackSpriteSheet.getSprite(0,0,self.width,self.height)
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

    def update(self):
        self.animate()
        self.collide()
    
    def collide(self):
        hits=pygame.sprite.spritecollide(self,self.game.enemies,True)
    
    def animate(self):
        direction=self.game.player.facing

        rightAnimations = [self.game.attackSpriteSheet.getSprite(0, 64, self.width, self.height),
                           self.game.attackSpriteSheet.getSprite(32, 64, self.width, self.height),
                           self.game.attackSpriteSheet.getSprite(64, 64, self.width, self.height),
                           self.game.attackSpriteSheet.getSprite(96, 64, self.width, self.height),
                           self.game.attackSpriteSheet.getSprite(128, 64, self.width, self.height)]

        downAnimations = [self.game.attackSpriteSheet.getSprite(0, 32, self.width, self.height),
                           self.game.attackSpriteSheet.getSprite(32, 32, self.width, self.height),
                           self.game.attackSpriteSheet.getSprite(64, 32, self.width, self.height),
                           self.game.attackSpriteSheet.getSprite(96, 32, self.width, self.height),
                           self.game.attackSpriteSheet.getSprite(128, 32, self.width, self.height)]

        leftAnimations = [self.game.attackSpriteSheet.getSprite(0, 96, self.width, self.height),
                           self.game.attackSpriteSheet.getSprite(32, 96, self.width, self.height),
                           self.game.attackSpriteSheet.getSprite(64, 96, self.width, self.height),
                           self.game.attackSpriteSheet.getSprite(96, 96, self.width, self.height),
                           self.game.attackSpriteSheet.getSprite(128, 96, self.width, self.height)]

        upAnimations = [self.game.attackSpriteSheet.getSprite(0, 0, self.width, self.height),
                         self.game.attackSpriteSheet.getSprite(32, 0, self.width, self.height),
                         self.game.attackSpriteSheet.getSprite(64, 0, self.width, self.height),
                         self.game.attackSpriteSheet.getSprite(96, 0, self.width, self.height),
                         self.game.attackSpriteSheet.getSprite(128, 0, self.width, self.height)]
        
        if direction=="up":
            self.image=upAnimations[math.floor(self.animationLoop)]
            self.animationLoop+=0.5
            if self.animationLoop>=5:
                self.kill()
        elif direction=="down":
            self.image=downAnimations[math.floor(self.animationLoop)]
            self.animationLoop+=0.5
            if self.animationLoop>=5:
                self.kill()
        elif direction=="left":
            self.image=leftAnimations[math.floor(self.animationLoop)]
            self.animationLoop+=0.5
            if self.animationLoop>=5:
                self.kill()
        elif direction=="right":
            self.image=rightAnimations[math.floor(self.animationLoop)]
            self.animationLoop+=0.5
            if self.animationLoop>=5:
                self.kill()

