import pygame
from configuration import *
from sprites import *
from GUI import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((screenWidth,screenHeight))
        self.windowName=pygame.display.set_caption("RPG Game")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont('Avenir',32)
        self.running=True

        self.characterSpriteSheet = SpriteSheet("img/character.png")
        self.terrainSpriteSheet = SpriteSheet("img/terrain.png")
        self.enemySpriteSheet = SpriteSheet("img/enemy.png")
        self.attackSpriteSheet = SpriteSheet("img/attack.png")
        self.introBackground=pygame.image.load('./img/introbackground.png')
        self.gameOverBackground=pygame.image.load('./img/gameover.png')

    def createTileMap(self):
        for row,i in enumerate(tileMap):
            for column,j in enumerate(i):
                Ground(self,column,row)
                if j=="B":
                    Block(self,column,row)
                elif j=="P":
                    self.player = Player(self,column,row)
                elif j=="E":
                    Enemy(self,column,row)

    def new(self):
        self.playing=True#starting new game

        self.allSprites=pygame.sprite.LayeredUpdates()
        self.blocks=pygame.sprite.LayeredUpdates()
        self.enemies=pygame.sprite.LayeredUpdates()
        self.attacks=pygame.sprite.LayeredUpdates()

        self.createTileMap()
    
    def events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if self.player.facing=='up':
                        Attack(self,self.player.rect.x,self.player.rect.y-tileSize)
                    if self.player.facing=='down':
                        Attack(self,self.player.rect.x,self.player.rect.y+tileSize)
                    if self.player.facing=='left':
                        Attack(self,self.player.rect.x-tileSize,self.player.rect.y)
                    if self.player.facing=='right':
                        Attack(self,self.player.rect.x+tileSize,self.player.rect.y)
                    
    def update(self):
        self.allSprites.update()
    def draw(self):
        self.screen.fill((0,0,0))
        self.allSprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update( )
    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
    def gameOver(self):
        title=self.font.render('Game Over',True,(0,0,0))
        titleRect=title.get_rect(center=(screenWidth/2,screenHeight/2))

        restartButton=Button(10,screenHeight-60,120,50,(255,255,255),(0,0,0),"Restart",32)

        for sprite in self.allSprites:
            sprite.kill()
        while self.running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False
            mousePos=pygame.mouse.get_pos()
            mousePressed=pygame.mouse.get_pressed()

            if restartButton.isPressed(mousePos,mousePressed):
                self.new()
                self.main()

            self.screen.blit(self.gameOverBackground,(0,0))
            self.screen.blit(title,titleRect)
            self.screen.blit(restartButton.image,restartButton.rect)
            self.clock.tick(FPS)
            pygame.display.update()


    def introScr(self):
        intro =True
        title=self.font.render('RPG',True,(0,0,0))
        titleRect=title.get_rect(x=10,y=10)
        playButton=Button(10,50,100,50,(255,255,255),(0,0,0),"Play",32)
        while intro:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    intro=False
                    self.running=False
            mousePos=pygame.mouse.get_pos()
            mousePressed=pygame.mouse.get_pressed()

            if playButton.isPressed(mousePos,mousePressed):
                intro=False
            self.screen.blit(self.introBackground,(0,0))
            self.screen.blit(title,titleRect)
            self.screen.blit(playButton.image,playButton.rect)
            self.clock.tick(FPS)
            pygame.display.update()



g=Game()
g.introScr()
g.new()
while g.running:
    g.main()
    g.gameOver()

pygame.quit()