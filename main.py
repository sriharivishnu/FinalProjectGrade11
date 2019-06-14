import pygame, pygame.gfxdraw, random, math#Imported modules

from Map import *
from Paintings import *
from Player import *
from Button import *
Guardwins =pygame.image.load("Guardwins.png")#render jail cell for endscreen when Guard wins
Mugshot=pygame.transform.scale(pygame.image.load("Mugshot.png"),(200,300))#render prisoner/Robber for endscreen when Guard wins

def printscore():#Prints score on endscreen
    generate_text("$"+str(player2_score),(WIDTH/2,400),(255,0,0),font1)#calls generate_text

def robberwin():#Prints robber win screen
    x=0
    for i in range(5):#create 6 money images on the screen
        load_image("Graphics/EndScreen/money.png",(x+WIDTH//4,HEIGHT*2/3+HEIGHT//4),2,)#call load_image
        x=x +WIDTH/6#go to the next position
    load_image("Graphics/EndScreen/frame.png", (WIDTH/2, 200),1)#load the frame
    generate_text("The robber wins!",(WIDTH/2, HEIGHT/2),(0,0,0),font1)#Print the robber wins on sreen

def guardwin():#Prints
    load_image("Graphics/EndScreen/bars.jpg",(WIDTH/2,HEIGHT/2),2/3)#draw bars
    generate_text("The guard wins!", (WIDTH / 2, HEIGHT / 2),(30,144,255),font1)#Print the guard wins

def generate_text(text,postion,color,font):#Generates incoming text
    text1 = font.render(text, False, color)#render text from incoming text and color
    text1_rect = text1.get_rect(center=(postion))#center text
    screen.blit(text1,(text1_rect))#blit text in center of screen

def load_image(image,postion,diveded_scale):#Blit incoming images
    image1 = pygame.image.load(image)#load the image
    image1 = pygame.transform.smoothscale(image1, (int(WIDTH // diveded_scale), int(HEIGHT //diveded_scale)))#Scale the image
    image1_rect = image1.get_rect(center=postion)#center image
    screen.blit(image1, image1_rect)#blit image in center of screen
#--------------------------------------------------------------------------------------------

def create_walls():#Creates the map
    global door
    Wall(0, 0, 32 * 32, 32, walls_sprites)#For some reason there were walls in the map, these patch them up
    Wall(0, 0, 32, 32 * 32, walls_sprites)
    Wall(32 * 31, 0, 32, 32 * 32, walls_sprites)
    Wall(0, 32 * 31, 32 * 32, 32, walls_sprites)
    #create the decorations in the corner
    #Wall(29 * 32, 27 * 32, 32*2, 32*2, tiles1, "Chair.png") 
    #Wall(29 * 32, (27-2) * 32, 32 * 2, 32 * 2, tiles1, "Checkers.png")
    #Wall(29 * 32, (27 + 2) * 32, 32 * 2, 32 * 2, tiles1, "Desk.png")
    
    #Read in map from map file
    lines = map.map_data.copy()
    lines.append(["." for z in range(len(lines[0]))])
    #Initialize array to hold temporary values of rect dimensions (Dynamic programming)
    current = [0 for z in range(len(lines[0]))]
    #Set array to initial values
    for x in range(len(lines[0])):
        #If there is a wall at the specified position add one in the respective position in the array
        if lines[0][x] == "#":
            current[x] += 1
    for y in range(1, len(lines)):
        #Set the width and height of the rectangle to 0
        width = 0
        value = 0
        for x in range(32):
            if lines[y][x] == "#":
                #If the width of a previous rectangle exists
                if width != 0:
                    Wall((x - width) * 32, (y - value) * 32, width * 32, value * 32, walls_sprites) #Create the wall
                    width = 0
                    value = 0
                current[x] += 1 #Add one to the temporary array

            else:
                if lines[y - 1][x] == "#": #If the line above is a wall
                    if value == 0:
                        value = current[x] #Height is of the previous wall
                        width += 1 #Add one to width of rectangle
                    else:
                        if current[x] != value:
                            Wall((x - width) * 32, (y - value) * 32, width * 32, value * 32, walls_sprites) #Create wall
                            value = current[x] #Height is of the previous wall
                            width = 1 #New width
                        else:
                            width += 1 #Add one to width
                elif lines[y - 1][x] != "#" and width != 0:
                    Wall((x - width) * 32, (y - value) * 32, width * 32, value * 32, walls_sprites) #Create new wall
                    width = 0
                    value = 0
                if lines[y][x] == "1":#if its a 1 print basic painting
                    Paintings(x * 32, y * 32, 32, 32, paintings_sprites, 1000)#create a basic painting in relation to where it is on the text document
                    #and make it 32x32 pixels and group it into paintings_sprites group, 1000 points
                elif lines[y][x] == "2":#If it's a 2 print medium painting
                    Paintings(x * 32, y * 32, 32, 32, paintings_sprites, 5000)
                elif lines[y][x] == "3":#Print the super painting(2x2)
                    Paintings(x * 32, y * 32, 32 * 2, 32 * 2, paintings_sprites, 50000)
                elif lines[y][x] == "d":#create an exit door
                    Wall(x * 32, y * 32, 32, 32, Exitdoors)
                elif lines[y][x] == "w":#create a basic White tile if w
                    Wall(x*32, y*32,32, 32, tiles1,"White")
                elif lines[y][x] == "E":#If E create the exitsign
                    Wall(x * 32, y * 32, 32, 32, Exits, "Exitsign.png",True)
                if lines[y][x] == "K":#If K create key
                    Key(x * 32, y * 32, 32, 32, paintings_sprites)
                if lines[y][x] == "D" and lines[y][x-1] == "D":#if there are two Ds in a row, create a vault door(2x1)
                    door=Door((x-1)*32, y*32, 32*2, 32, walls_sprites)#create a 2x1 door at the previous location in the walls_sprites group
                current[x] = 0
        if width != 0: #If there is still a wall not created
            Wall((len(lines[0]) - width) * 32, (y - value) * 32, width * 32, value * 32, walls_sprites) #Create wall
WIDTH_LIGHT = 30 #Max width of light
MAX_DISTANCE = 100 #Length of light
FPS = 20#FPS Cap

def calculate_angle(x1,y1,x2,y2):#calculate angle between mouse and player
    if x1 - x2 != 0:#if it's not 0(division error)
        y = y1 - y2#get y component of vector
        x = x1 - x2#get x component of vector
        angle = math.degrees(math.atan(y / x))#get angle of slope
        if x < 0 and y > 0 or x < 0 and y < 0:#Tangent math exception
            angle += 180#add 180 to angle
        return angle
    return None#if it's zero, return none

def get_light(center, angle)#Raycasting Function
    pointlist = [center]#Add the Player's location to the list of points to create the polygon(make the flashlight originate from the
    #character)
    hit_player = False#Used in testing if player has been seen by flashlight
    for x in range(-1*WIDTH_LIGHT, WIDTH_LIGHT+1,2):#Test in a range of angles, test every other angle
        current = angle + x#current angle
        hit = False#used for double break
        targetposy = center[1] + (2 * math.sin(math.radians(current)) * MAX_DISTANCE)#target of ray being cast out
        targetposx = center[0] + (2 * math.cos(math.radians(current)) * MAX_DISTANCE)
        xdisp = (targetposx - center[0]) / MAX_DISTANCE#speed of ray
        ydisp = (targetposy - center[1]) / MAX_DISTANCE
        for y in range(0,MAX_DISTANCE,2):#test multiple points between the player and the target position to see if they hit a wall/player
            for wall in renderlist:#check if that point is hitting any wall that's in a rectangular area in front of the player
                point = [center[0] + xdisp * y, center[1] + ydisp * y]#creates the current point that is checking collision
                if camera.apply(wall).collidepoint(point[0], point[1]):#if the point collides with a wall
                    pointlist.append(point)#append it to the list of points for the polygon
                    hit = True#Double Break/new angle
                    break
                if camera.apply(player2).collidepoint(point[0], point[1]):#if the point collides with a player
                    pointlist.append(point)#append the point to the list of points
                    hit = True#double break
                    hit_player = True#used for making the player appear
                    break
            if hit:
                break#double break
        if not hit:
            pointlist.append([targetposx, targetposy])#if nothing has been hit append the target position to the list of points
            #acts as "uninterupted" light
    if not hit_player:
        hit_player = False

    return pointlist, hit_player#return list for polygon, hit_player for showing the Robber on the Guard's screen

def tilesrender():#Test if player collides with a lit up decorative tile
    for tile in tiles1:#for every tile in decorative tile lest
        if camera.apply(player2).colliderect(camera.apply(tile)):#if the robber is inside a decorative tile
            return True#blit the robber on the other player's sceen
    return False#else don't


def check_collisions():#check for collision of guard with walls and doors
    copy = player.rect.copy()#create a copy of the player's rect
    copy2 = player.rect.copy()
    collidesx = False
    collidesy = False
    copy.x = position[0] + player.xvel - player.rect.width / 2#creates a predictioon of the player's next location
    copy2.y = position[1] + player.yvel - player.rect.height / 2
    for wall in renderlist:#for each wall that is in an area in front of the Guard, a bit around him
        if camera.apply_rect(copy).colliderect(camera.apply(wall)):#if the player is about to collide with a wall in the x plane
            collidesx = True
            player.bouncex()#reverse x velocity
        if camera.apply_rect(copy2).colliderect(camera.apply(wall)):#if the player is about to collide with a wall in the y plane
            collidesy = True
            player.bouncey()#reverse y velocity
    if Exitdoors:#same as above but with Exitdoors(act as walls but can be opened)
        for wall in Exitdoors:
            if camera.apply_rect(copy).colliderect(camera.apply(wall)):
                collidesx = True
                player.bouncex()
            if camera.apply_rect(copy2).colliderect(camera.apply(wall)):
                collidesy = True
                player.bouncey()
    #If the Guard has not collided with anything, keep the same velocity.
    if not collidesx:
        player.position[0] += player.xvel

    if not collidesy:
        player.position[1] += player.yvel

#same as above check_collision() but with Robber
def check_collisions2():
    copy = player2.rect.copy()
    copy2 = player2.rect.copy()
    collidesx = False
    collidesy = False
    copy.x = position2[0] + player2.xvel - player2.rect.width / 2
    copy2.y = position2[1] + player2.yvel - player2.rect.height / 2
    for wall in renderlist_player2:
        if camera2.apply_rect(copy).colliderect(camera2.apply(wall)):
            collidesx = True
            player2.bouncex()
        if camera2.apply_rect(copy2).colliderect(camera2.apply(wall)):
            collidesy = True
            player2.bouncey()
    if Exitdoors:
        for wall in Exitdoors:
            if camera2.apply_rect(copy).colliderect(camera2.apply(wall)):
                collidesx = True
                player2.bouncex()
            if camera2.apply_rect(copy2).colliderect(camera2.apply(wall)):
                collidesy = True
                player2.bouncey()

    if not collidesx:
        player2.position[0] += player2.xvel

    if not collidesy:
        player2.position[1] += player2.yvel

def create_render():#creates the odd shaped render box 
    changex = 0
    changey = 0
    #gets the positions of the edges of the flashlight from angle between mouse and Guard, taking the extremes of the angle(left most of flashlight, rightmost of flashlight.
    targetposy1 = actual.y + (2 * math.sin(math.radians(targetangle + -1 * WIDTH_LIGHT)) * (MAX_DISTANCE + 20))
    targetposx1 = actual.x + (2 * math.cos(math.radians(targetangle + -1 * WIDTH_LIGHT)) * (MAX_DISTANCE + 20))
    targetposx2 = actual.x + (2 * math.cos(math.radians(targetangle + WIDTH_LIGHT)) * (MAX_DISTANCE + 20))
    targetposy2 = actual.y + (2 * math.sin(math.radians(targetangle + WIDTH_LIGHT)) * (MAX_DISTANCE + 20))
    maxx = max(targetposx1, targetposx2, actual.x)#Get the biggest x coordinate
    miny = min(targetposy1, targetposy2, actual.y)#Smallest y
    minx = min(targetposx1, targetposx2, actual.x)#Smallest x
    maxy = max(targetposy1, targetposy2, actual.y)#Biggest y
    diffx = maxx - minx#distance between biggest x, smallest y
    diffy = maxy - miny#distance between biggest y, smallest y
    
    #create a box with the corner of biggest x, smallest y coordinate and lengths of differences between extremes
    return pygame.Rect(maxx + changex - MAX_DISTANCE*2, miny + changey, diffx,diffy)

def update_screen():
    # rendering for player 1
    for sprite in walls_sprites:#for every wall
        #if the wall is within the render boxes(1 in direction of player, other very small one around the player
        if render.colliderect(camera.apply(sprite)) or renderwalls.colliderect(camera.apply(sprite)):
            renderlist.add(sprite)#add the wall to the renderlist so it will be rendered, used for flashlight raytracing
        else:#otherwise
            renderlist.remove(sprite)#don't render the wall/use for flashlight raytracing
    for painting in paintings_sprites:#same as wall rendering, but instead rendering paintings
        if render.colliderect(camera.apply(painting)) or renderwalls.colliderect(camera.apply(painting)):
            paintrenderlist.add(painting)
        else:
            paintrenderlist.remove(painting)

    # rendering for player 2
    #same as rendering for player 1, but with a single hitbox in a larger area
    for sprite in walls_sprites_player2:
        if render2.colliderect(camera2.apply(sprite)):
            renderlist_player2.add(sprite)
        else:
            renderlist_player2.remove(sprite)
    for painting in paintings_sprites_player2:
        if render2.colliderect(camera2.apply(painting)):
            paintrenderlist_player2.add(painting)
        else:
            paintrenderlist_player2.remove(painting)
    
    #update player sprites
    sprites.update()
    sprites2.update()
    
    #update the cameras
    camera.update(player, WIDTH, HEIGHT)
    camera2.update(player2, WIDTH, HEIGHT)

def draw_screen():#draw the screens
    global health
    global seen
    screen.fill((255,255,255))#fill the screen
    box_surface_fill = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)#used for creating a transparent flashlight
    player1surface.fill((0, 0, 0))#fill first player split screen with black(darkness)
    player2surface.fill((123, 204, 128))#other with green (night vision)
    pygame.draw.polygon(box_surface_fill, (255, 255, 100, max(0, min(brightness, 255))), pointlist)#draw a polygon/flashlight 
    #using collision pointlist
    player1surface.blit(box_surface_fill, (0, 0))#blit the flashlight surface on the Guard's screen
    if Exitdoors:#If there are any exidoors(may be killed after getting enough points)
        for tile in Exitdoors:#For every exitdoor
            #blit the Exidoors on both player's surfaces
            player1surface.blit(tile.image, camera.apply(tile))
            player2surface.blit(tile.image, camera2.apply(tile))
    
    for tile in tiles1:#For every decorative tile
        #blit decorative tile on both screens
        player1surface.blit(tile.image, camera.apply(tile))
        player2surface.blit(tile.image, camera2.apply(tile))
    for sprite in sprites:#blits Guard on Guard Screen
        player1surface.blit(sprite.image, camera.apply(sprite))
    for wall in renderlist:#For all walls in the first player's render area
        player1surface.blit(wall.image, camera.apply(wall))#blit the wall
    for painting in paintrenderlist:#same as above but for painting
        player1surface.blit(painting.image, camera.apply(painting))
    if battery>=10:#If the robber's night vision is charged
        for wall in renderlist_player2:#for every wall on the Robber's Screen
            player2surface.blit(wall.image,camera2.apply(wall))#blit the wall
        for painting in paintrenderlist_player2:#For paintings on the robber's screen
            player2surface.blit(painting.image,camera2.apply(painting))#blit the painting
        #Blits both of the players on the Robber's screen   
        player2surface.blit(player2.image,camera2.apply(player2))
        player2surface.blit(player.image, camera2.apply(player))

    if battery<=0:#if the player's battery is completely out
        player2surface.fill((0,0,0))#make the player's screen black
        player2surface.blit(Notification,(0,0))#display a notification for them to charge
    else:
        player2surface.blit(Night_vision, (-100, -100))#if it's not out blit the transparent night vision scope
    for Exitss in Exits:#for all exit signs
        player1surface.blit(Exitss.image, camera.apply(Exitss))#blit exit sign
        player2surface.blit(Exitss.image, camera2.apply(Exitss))
    if flash_collide or tilesrender():
        if flash_collide:
            health-=.05
        player1surface.blit(player2.image, camera.apply(player2))#draw player on other side
        if seen!=True:#if you are seen for the first time
            seen=True
            pygame.mixer.music.play()#Play alert theme

        if battery<=0:#if the player's night vision is down, they are in flashlight
            player2surface.blit(player2.image, camera2.apply(player2))#make them appear

    box_surface_fill = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)#create the surface on which the flashlight is blitted(for enemy)
    pygame.draw.polygon(box_surface_fill, (200, 255, 200, max(0, min(brightness, 255))), pointlist)#This time it is white to simulate
    #bright light when using night vision
    player2surface.blit(box_surface_fill, (-camera.camera.x + camera2.camera.x, -camera.camera.y + camera2.camera.y))#^
    #blit both splitscreens on screen
    screen.blit(player2surface,(0,0))
    screen.blit(player1surface, (WIDTH//2, 0))

#Width, Height of screen
WIDTH = 1000
HEIGHT = 500

#split screeens half the screen
player1surface=pygame.Surface([WIDTH/2,HEIGHT])#Player 1 split screen side
player2surface=pygame.Surface([WIDTH/2,HEIGHT])#Player 2 split screen side

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("Audio/Alert theme.mp3")

health=5#health of Robber
Notification=pygame.image.load("Graphics/Game Images/Notification.png")#Load notification image
Night_vision=pygame.transform.scale(pygame.image.load("Graphics/Game Images/Night Vision Scope.png"),(700,700))#Adds night vision effect

screen = pygame.display.set_mode([WIDTH, HEIGHT])#create screen

walls = []
map = Map()

#create the sprite groups
tiles1=pygame.sprite.Group()#group for decorative tiles
Exits=pygame.sprite.Group()#Exit sign group
Exitdoors=pygame.sprite.Group()#Exit doors group
center = [WIDTH/2, HEIGHT/2]
mouse_position = center
sprites = pygame.sprite.Group()#Group for player sprites
renderlist = pygame.sprite.Group()#Render list for walls
paintrenderlist=pygame.sprite.Group()#Render list for paintings
renderlist_player2= pygame.sprite.Group()#Render list for player 2 walls
walls_sprites = pygame.sprite.Group()#Group for walls
paintings_sprites = pygame.sprite.Group()#Painting sprite group
paintrenderlist_player2=pygame.sprite.Group()#render list for player two paintings
door = [0]#This is needed for some weird reason
create_walls()#Create the map

#Create copies of groups for player 2
walls_sprites_player2 = walls_sprites.copy()
paintings_sprites_player2 = paintings_sprites.copy()
sprites2=pygame.sprite.Group()
player = Player([500,500], 20, 1)#Create player sprites/Note:use first two variables to change spawn position
sprites.add(player)
player2 = Player([700, 700], 20, 2)#same as above
sprites2.add(player2)
render = pygame.Rect(WIDTH/2 - MAX_DISTANCE * 2, HEIGHT/2 - MAX_DISTANCE * 2, MAX_DISTANCE * 4,MAX_DISTANCE * 4)#???????????
render2 = pygame.Rect((0,0),([WIDTH/2,HEIGHT]))#render box for the entire splitscreen of Robber
renderwalls=pygame.Rect(0, 0, 50,50)#render small player1 render box

#Create both cameras
camera = Camera(WIDTH, HEIGHT)
camera2 = Camera(WIDTH, HEIGHT)

targetangle = 260#random target angle so it doesn't crash
crashed = False
brightness = 180#Brightness of flashlight.
flash_collide = False
player2_score = 0#Player score is 0
clock = pygame.time.Clock()#set up clock
actual = camera.apply(player)#actual position of player in relation to the map
seen = False#used for playing alert music

font = pygame.font.SysFont(None,50)#create font
battery=200#battery charge total
charging=False#Charging boolean to keep player from moving when charging

#Load images for instructions
Introscreen1=pygame.transform.scale(pygame.image.load("Graphics/Intro Images/Intro Screen.png"),(700,HEIGHT))
road=pygame.transform.scale(pygame.image.load("Graphics/Intro Images/Road.png"),(1000,HEIGHT))
car=pygame.transform.scale(pygame.image.load("Graphics/Intro Images/Car.png"),(100,100))
robberinstructions=pygame.image.load("Graphics/Intro Images/Robberslide1.png")
road2=road#copy of road for scrolling image(make it look like car is moving down a road)
button1=pygame.Rect((250,20),(450,HEIGHT-50))#rect on top of painting to click to start game
Unclicked=True

#Introduction scenes--------------------------------------------------------------------------------------
while Unclicked:#First loop of introduction(shows the painting with GO on it)
    screen.fill((0,0,0))#Fill background
    screen.blit(Introscreen1,(140,0))#blit the painting/intro screen
    #pygame.draw.rect(screen, (125, 124, 200), button1, 1)used for debuging(to show rectangle/button area)
    for event in pygame.event.get():#event loop for checking if player presses painting
        if event.type == pygame.MOUSEBUTTONDOWN:#if the player clicks
            if button1.collidepoint(pygame.mouse.get_pos()):#Check if they are clicking the painting
                Unclicked=False#make it so that it won't loop again/move on to instructions
                for x in range(0,800,10):#make the paintings move off screen, road move into screen when clicked
                    screen.fill((0, 0, 0))
                    screen.blit(road, (600-x, 0))#blit both roads gradually leftwards
                    screen.blit(road2, (600+200 - x, 0))
                    screen.blit(Introscreen1, (140-x, 0))#blit painting gradually leftwards
                    pygame.display.flip()#update screen

    pygame.display.flip()#update screen
    
#reseting, setting up variables
Unclicked=True
disp=0
cardisp=0
cardispy=0
cardispconst=0.5
cardispconsty=0.5
slide=1
button=buttons(350,50,(0,0,0),"Click to continue",650,400,(255,255,255))#create button

while Unclicked:#loop for instrucctions

    for event in pygame.event.get():#event loop, checking if mouse or left, right and space key have been pressed
        if event.type == pygame.MOUSEBUTTONDOWN:#if the mouse is pressed
            if button.rect.collidepoint(pygame.mouse.get_pos()) and slide>4:#if the mouse is colliding with the button, is on the final slide
                Unclicked=False#end loop, move on to cop instructions
        if event.type == pygame.KEYDOWN:#if any button is pressed
            if event.key==pygame.K_SPACE or event.key==pygame.K_RIGHT:#if it's a space or right key
                slide+=1#move forward one slide
            if event.key==pygame.K_LEFT and slide>1:#if you press left and you're not on the first slide
                slide-=1#move back one slide
    #Used to bounce car back and forth to make it look like it's driving around
    if cardisp==-20 or cardisp== 20:#if it's at an extreme x position
        cardispconst*=-1 #inverse x "velocity"
    if cardispy==-10 or cardispy==10:#same as above, a little less bouncing
        cardispconsty*=-1 #inverse y "velocity"
    
    #displace car by velocity
    cardisp+=cardispconst
    cardispy+=cardispconsty
    
    disp+=5#displacement of road images by 5
    if disp>=1000: #if a road has moved across the entire screen 
        disp=0 #loop it around/teleport it to the start again to give an infinite road effect
    screen.fill((0, 0, 0))
    
    #blit roads, car with displacement
    screen.blit(road, (0-disp, 0))
    screen.blit(road2, (0+1000 - disp, 0))
    screen.blit(car,(WIDTH//2-cardisp,HEIGHT//2+100-cardispy))
    
    #flip through slides
    if slide==1:
        robberinstructions=pygame.image.load("Graphics/Intro Images/Robberslide1.png")#load associated slide
    elif slide==2:
        robberinstructions=pygame.image.load("Graphics/Intro Images/Robberslide2.png")
    elif slide==3:
        robberinstructions=pygame.image.load("Graphics/Intro Images/Robberslide3.png")
    elif slide==4:
        robberinstructions=pygame.image.load("Graphics/Intro Images/Robberslide4.png")
    else:
        screen.blit(button.surface,(button.x,button.y))#on final slide show the button
    screen.blit(robberinstructions,(0,0))#blit currently loaded slide
    pygame.display.flip()#update screen
    
Unclicked=True#make unclicked true again
Guardinstructions=pygame.image.load("Graphics/Intro Images/Guardinstructions.png")
button=buttons(180,50,(255,255,0),"Click to continue",350,450,(0,0,0),"Arial",28)#create new button in different location

while Unclicked:#loop for showing instructions for guard
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:#if the mouse is clicked
            if button.rect.collidepoint(pygame.mouse.get_pos()):#if you clicked on a button
                Unclicked=False#exit the loop, get into main game loop
    screen.fill((255,255,255))#fill screen with white
    screen.blit(Guardinstructions,(0,0))#blit guard instructions
    screen.blit(button.surface,(button.x,button.y))#blit button
    pygame.display.flip()#update screen
#End of introduction--------------------------------------------------------------------------------------

win=False

#MAIN LOOP------------------------------------------------------------------------------------------------
while not crashed:
    for event in pygame.event.get():#main event loop
        if event.type == pygame.QUIT:#if you press quit, quit the game
            crashed = True#end the game loop 
        if event.type == pygame.MOUSEMOTION:#if you move your mouse
            mouse_position = event.pos#get a new mouse position
        if event.type == pygame.KEYDOWN:#if you press down a button
            if event.key == pygame.K_f:#if it's f charge the Night vision
                charging=True
            elif charging!=True:#If you are not holding down the f button(to keep Robber from charging Night vision and moving)
                if event.key == pygame.K_SPACE:#if the player presses space
                    for painting in paintrenderlist_player2:#for every painting that is visible for the player
                        if camera2.apply(player2).colliderect(camera2.apply(painting)):#check what painting the player is ontop of
                            #kill the painting from all groups
                            paintings_sprites_player2.remove(painting)
                            paintrenderlist_player2.remove(painting)
                            paintings_sprites.remove(painting)
                            paintrenderlist.remove(painting)
                            
                            player2_score += painting.points#add the painting's score to the Robber's score
                            
                            if painting.points == 0:#if it has 0 points(meaning it's a key)
                                key_obtained = True #state that the key has been obtained
                                door.rect.x=1000000#move the door off the map so that it's "open"
                            break#stop searching for paintings

        if event.type == pygame.KEYUP:#if you unpress key
            if event.key == pygame.K_f:#if it's the f key
                charging=False#stop charging


    player.move(pygame.key.get_pressed(), 2)#move player according to their key press
    if not charging: #If you are not holding down the f button(to keep Robber from charging Night vision and moving)
        player2.move(pygame.key.get_pressed(), 1)#same as player.move but with Robber
    
    #position of players
    position = player.get_position()
    position2 = player2.get_position()
    
    actual = camera.apply(player)#actual position of player in relation to the map
    
    #calculate new angle
    new_angle = calculate_angle(mouse_position[0], mouse_position[1], actual.x + player.width+WIDTH//2, actual.y + player.width)
    if new_angle:
        targetangle = new_angle
    
    
    player.rotate(-targetangle)#rotate Guard to the mouse
    render = create_render()#creates render box for player 1 (flashlight render shape)
    actual2 = camera2.apply(player2)#actual position of player 2 in relation to the map
    render2.center = [WIDTH//4,HEIGHT//2]#center of the render box for the Robber
    pointlist,flash_collide = get_light([actual.x + player.width // 2, actual.y + player.width // 2], targetangle)#draw flashlight
    renderwalls.center=[actual.x+10,actual.y+10]#the center of the small render box for the Guard becomes the player's center
    
    #check collisions for both players
    check_collisions()
    check_collisions2()

    draw_screen()#draw screen
    update_screen()
    clock.tick(FPS)#limit clock at the FPS cap
    if battery>0: #if the battery is not at 0
        battery-=0.5 #decrease the battery by 0.5
    if charging and battery<200:#if the player is holding f and they aren't fully charged
        battery += 1.5 #charge the battery 1.5
    if battery>20:#if the battery is above 20
        night_vision_counter = font.render(str(round(((battery/200)*100)))+"% Charge", True, (255,255,255), (0, 0, 0)) #make the charge black
         #the charge is displayed as a percent of the maximum charge
    else:
        night_vision_counter = font.render(str(round(((battery / 200) * 100))) + "% Charge", True, (255, 0, 0),
                                           (0, 0, 0)) #else make it red
    screen.blit(night_vision_counter, (0, 0)) #blit the percent charge
    if player2_score>=20000: #if the Robber has a score of atleast 20000
        Exitdoors=None #kill all the doors in Exitdoors group so Robber can escape
        if player2.get_position()[0]<=0: #if the player is out of the map
            win=True #they win
            crashed=True #exit the game loop
    if health<=0:#if the Robber is caught
        crashed=True #exit the game loop without win=True (Robber looses)
    pygame.display.flip() #update screen

done=False

#create 2 fonts for the endscreen
font1 = pygame.font.SysFont("Arial", 60)
font2 = pygame.font.SysFont("Arial", 80)


WIDTH=500
HEIGHT=500

Firsttime=True

while not done: #final loop for endscreen

    for event in pygame.event.get():#event loop for pressing quit
        if event.type == pygame.QUIT:#if you press quit
            done = True # quit the loop, game
    if win==True: #if the Robber won
        robberwin() #print the robberwin screen
        printscore() #print the score
        generate_text("game over", (WIDTH / 2, HEIGHT / 3 - 50), (0, 125, 0), font2) #print "game over"
    elif win==False and Firsttime: #Firstime so it only runs once
        pygame.mixer.music.load("Prison cell door sound effect.mp3")#load jail cell noise
        pygame.mixer.music.play(0)#play once
        for m in range(-500,0,2):#move a cage gradually over a mugshot of a thief
            screen.fill((255, 255, 255)) #fill the screen with white
            screen.blit(Mugshot,(300,HEIGHT-300))#blit mugshot of robber
            screen.blit(Guardwins,(200,0+m))#blit the cage, with displacement m to make it seem like it's going down
            pygame.display.flip()#update screen
        Firsttime=False#make it so that it won't run again, will stay at a still image of a jail cell over the criminal
