from main import *

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