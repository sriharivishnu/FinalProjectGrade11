# Player class to define players
import pygame
import math
class Player(pygame.sprite.Sprite):
    #Player constants
    FRICTION = 0.75
    MAX_VELOCITY = 5
    ACCELERATION = 1.5
    
    #Init function: Use parameters position
    def __init__(self, position, width, player):
        pygame.sprite.Sprite.__init__(self)
        #Create an image surface
        self.image = pygame.Surface([width, width], pygame.SRCALPHA)
        #If the player is the cop
        if player == 1:
            #Blit the appropriate img
            self.image.blit(pygame.transform.scale(pygame.image.load("Graphics/Game Images/guard_image.png"), (width, width)), (0,0))
        #Otherwise, player is the robber
        else:
            #Blit the robber img
            self.image.blit(pygame.transform.scale(pygame.image.load("Graphics/Game Images/robber_image.png"), (width, width)), (0,0))
        
        #Various other variables to keep track of player
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.width = width
        self.rect.center = position
        self.xvel = 0
        self.yvel = 0
        self.position = position
        self.angle = 0
        self.deceleration = True

    # Accelerate forward in the direction the player is facing
    def thrust(self):
        # Calculate the horizontal component of velocity
        self.xvel = self.xvel + self.ACCELERATION * math.cos(math.radians(self.angle))
        # Calculate the vertical component of velocity
        self.yvel = self.yvel + self.ACCELERATION * math.sin(math.radians(-self.angle))

        # Make sure the velocities doesn't go above the max velocity
        if self.xvel > self.MAX_VELOCITY:
            self.xvel = self.MAX_VELOCITY
        if self.xvel < -self.MAX_VELOCITY:
            self.xvel = -self.MAX_VELOCITY
        if self.yvel > self.MAX_VELOCITY:
            self.yvel = self.MAX_VELOCITY
        if self.yvel < -self.MAX_VELOCITY:
            self.yvel = -self.MAX_VELOCITY
    
    #Bounce player in the x direction by negating x velocity
    def bouncex(self):
        self.xvel = -self.xvel
    
    #Bounce player in the y direction by negating y velocity
    def bouncey(self):
        self.yvel = -self.yvel
    
    #Rotate player right and move right
    def move_right(self):
        self.angle = 0
        self.thrust()
    
    #Rotate player up and move up
    def move_up(self):
        self.angle = 90
        self.thrust()
    
    #Rotate player left and move left
    def move_left(self):
        self.angle = 180
        self.thrust()
    
    #Rotate player down and move down
    def move_down(self):
        self.angle = 270
        self.thrust()
    
    #Rotate player to a desired angle
    def rotate(self, angle):
        self.angle = angle
    
    #Move player according to what key was pressed
    def move(self, keys, player):
        if player == 1:
            if keys[pygame.K_a]:
                self.move_left()
            if keys[pygame.K_d]:
                self.move_right()
            if keys[pygame.K_w]:
                self.move_up()
            if keys[pygame.K_s]:
                self.move_down()
        else:
            if keys[pygame.K_LEFT]:
                self.move_left()
            if keys[pygame.K_RIGHT]:
                self.move_right()
            if keys[pygame.K_UP]:
                self.move_up()
            if keys[pygame.K_DOWN]:
                self.move_down()
    
    #Return position
    def get_position(self):
        return self.position
    
    #Set position of player
    def set_position(self, x, y):
        self.position = [x, y]

    # Called every frame
    def update(self, *args):

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        # Get new rect object
        self.rect = self.image.get_rect()
        # Set the rect center to the new position
        self.rect.center = self.position

        # Decrease velocity every frame by the friction of the surface as long as its
        # greater than 0
        if self.deceleration:
            #If x velocity is close to 0 just set to 0
            if -1 < self.xvel < 1:
                self.xvel = 0
            #Apply friction depending on direction
            elif self.xvel >= 1:
                self.xvel -= self.FRICTION
            else:
                self.xvel += self.FRICTION
            
            #If y velocity is close to 0 set to 0 exact
            if -1 < self.yvel < 1:
                self.yvel = 0
            #Apply friction depending on direction
            elif self.yvel >= 1:
                self.yvel -= self.FRICTION
            else:
                self.yvel += self.FRICTION
