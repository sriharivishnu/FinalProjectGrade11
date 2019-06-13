import pygame
# Wall class to define walls
class Wall(pygame.sprite.Sprite):
    #Init position, dimensions
    def __init__(self, x,y, width, height, group,image=None,small=None):
        self.groups = group
        #Init from super class
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)

        
        if image!=None:
            if image=="White":
                self.image.fill((255,255,255))
            elif small:
                self.image.blit(pygame.transform.scale(pygame.image.load(image), (25,32)), (0, 0))
            else:
                self.image.blit(pygame.transform.scale(pygame.image.load(image),(32*2,2*32)),(0,0))
        else:
            self.image.fill((25, 25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#Door class
class Door(pygame.sprite.Sprite):
    def __init__(self, x,y, width, height, group):
        self.groups = group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((width,height), pygame.SRCALPHA)
        self.image.blit(pygame.transform.scale(pygame.image.load("Graphics/Game Images/door.png"),(32*2,32)),(0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
#Map class to handle map
class Map:
    def __init__(self):
        self.map_data = []
        with open("maps.txt", "r") as file:
            for line in file:
                self.map_data.append(line)

        self.width = len(self.map_data[0]) * 32
        self.height = len(self.map_data) * 32

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0,0, width, height)
        self.width = width
        self.height = height

    def apply(self, sprite):
        new_rect = pygame.Rect(sprite.rect.x + self.camera.x, sprite.rect.y + self.camera.y, sprite.rect.width, sprite.rect.height)
        return new_rect

    def apply_rect(self, obj):
        return pygame.Rect(obj.x + self.camera.x, obj.y + self.camera.y, obj.width, obj.height)

    def update(self, target, screenw, screenh):
        x = -target.rect.x + screenw // 4
        y = -target.rect.y + screenh // 2

        x = max(min(0,x), - (32*32 - screenw//2))
        y = max(min(0,y), - (32*32 - screenh))
        self.camera = pygame.Rect(x,y, self.width, self.height)
