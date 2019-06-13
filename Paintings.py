import pygame
import random

class Paintings(pygame.sprite.Sprite):#create paintings
    #All the images prestored and ready to go
    Paints = [(pygame.transform.scale(pygame.image.load("Graphics/Painting Images/Paint1.png"), (32 * 2, 2 * 32))),
              (pygame.transform.scale(pygame.image.load("Graphics/Painting Images/Paint2.png"), (32, 32))),
              (pygame.transform.scale(pygame.image.load("Graphics/Painting Images/Paint3.png"), (32, 32))),
              (pygame.transform.scale(pygame.image.load("Graphics/Painting Images/Paint4.png"), (32, 32))),
              (pygame.transform.scale(pygame.image.load("Graphics/Painting Images/Paint5.png"), (32, 32))),
              (pygame.transform.scale(pygame.image.load("Graphics/Painting Images/Paint6.png"), (32, 32))),
              (pygame.transform.scale(pygame.image.load("Graphics/Painting Images/Paint7.png"), (32, 32))),
              (pygame.transform.scale(pygame.image.load("Graphics/Painting Images/Paint8.jpg"), (32, 32))),
              (pygame.transform.scale(pygame.image.load("Graphics/Painting Images/Paint9.jpg"), (32, 32))),
              (pygame.transform.scale(pygame.image.load("Graphics/Painting Images/Paint10.jpg"), (32, 32))),
              (pygame.transform.scale(pygame.image.load("Graphics/Painting Images/Paint11.jpg"), (32, 32)))]\
    #Init function with parameters of position, dimensions, group, and its painting value
    def __init__(self,x,y,width,height,group,points):
        #Assign to instance
        self.groups = group
        #Super class init
        pygame.sprite.Sprite.__init__(self, self.groups)
        #Create image
        self.image = pygame.Surface((width, height),pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.points=points
        #If the painting is worth 1000 points, put the appropriate image and border
        if self.points==1000:
            self.image.blit(self.Paints[random.randint(5,10)], (0,0))
            self.image.blit(pygame.transform.scale(pygame.image.load("Graphics/Painting Images/painting1.png"),(32,32)),(0,0))
        #If the painting is worth 5000 points, put the appropriate image and border
        elif self.points==5000:
            self.image.blit(self.Paints[random.randint(1, 4)], (0, 0))
            self.image.blit(pygame.transform.scale(pygame.image.load("Graphics/Painting Images/painting2.png"),(32,32)),(0,0))
        #If the painting is worth 50000 points, put the appropriate image and border
        elif self.points==50000:
            self.image.blit(self.Paints[0], (0, 0))
            self.image.blit(pygame.transform.scale(pygame.image.load("Graphics/Painting Images/painting3.png"),(32*2,2*32)),(0,0))

#Key class
class Key(pygame.sprite.Sprite):#create key
    def __init__(self,x,y,width,height,group):
        self.groups = group
        pygame.sprite.Sprite.__init__(self, self.groups)
        #Create image and appropriate rect coordinates
        self.image = pygame.Surface((width, height),pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #Blit the image
        self.image.blit(pygame.transform.scale(pygame.image.load("Graphics/Game Images/key.png"), (32, 32)), (0,0))
        self.points = 0
