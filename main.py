import pygame, pygame.gfxdraw, random, math

from Map import *
from Paintings import *
from Player import *
from Button import *
#for printing end
def printscore():
    generate_text("$"+str(player2_score),(WIDTH/2,400),(255,0,0),font1)

def robberwin():
    x=0
    for i in range(5):
        load_image("Graphics/EndScreen/money.png",(x+WIDTH//4,HEIGHT*2/3+HEIGHT//4),2,)
        x=x +WIDTH/6
    load_image("Graphics/EndScreen/frame.png", (WIDTH/2, 200),1)
    generate_text("The robber wins!",(WIDTH/2, HEIGHT/2),(0,0,0),font1)

def guardwin():
    load_image("Graphics/EndScreen/bars.jpg",(WIDTH/2,HEIGHT/2),2/3)
    generate_text("The guard wins!", (WIDTH / 2, HEIGHT / 2),(30,144,255),font1)

def generate_text(text,postion,color,font):
    text1 = font.render(text, False, color)
    text1_rect = text1.get_rect(center=(postion))
    screen.blit(text1,(text1_rect))

def load_image(image,postion,diveded_scale):
    image1 = pygame.image.load(image)
    image1 = pygame.transform.smoothscale(image1, (int(WIDTH // diveded_scale), int(HEIGHT //diveded_scale)))
    image1_rect = image1.get_rect(center=postion)
    screen.blit(image1, image1_rect)
#--------------------------------------------------------------------------------------------

def create_walls():
    global door
    Wall(0, 0, 32 * 32, 32, walls_sprites)
    Wall(0, 0, 32, 32 * 32, walls_sprites)
    Wall(32 * 31, 0, 32, 32 * 32, walls_sprites)
    Wall(0, 32 * 31, 32 * 32, 32, walls_sprites)
    #Wall(29 * 32, 27 * 32, 32*2, 32*2, tiles1, "Chair.png")
    #Wall(29 * 32, (27-2) * 32, 32 * 2, 32 * 2, tiles1, "Checkers.png")
    #Wall(29 * 32, (27 + 2) * 32, 32 * 2, 32 * 2, tiles1, "Desk.png")

    lines = map.map_data.copy()
    lines.append(["." for z in range(len(lines[0]))])
    current = [0 for z in range(len(lines[0]))]
    for x in range(len(lines[0])):
        if lines[0][x] == "#":
            current[x] += 1
    for y in range(1, len(lines)):
        width = 0
        value = 0
        for x in range(32):
            if lines[y][x] == "#":
                if width != 0:
                    Wall((x - width) * 32, (y - value) * 32, width * 32, value * 32, walls_sprites)
                    width = 0
                    value = 0
                current[x] += 1

            else:
                if lines[y - 1][x] == "#":
                    if value == 0:
                        value = current[x]
                        width += 1
                    else:
                        if current[x] != value:
                            Wall((x - width) * 32, (y - value) * 32, width * 32, value * 32, walls_sprites)
                            value = current[x]
                            width = 1
                        else:
                            width += 1
                elif lines[y - 1][x] != "#" and width != 0:
                    Wall((x - width) * 32, (y - value) * 32, width * 32, value * 32, walls_sprites)
                    width = 0
                    value = 0
                if lines[y][x] == "1":
                    Paintings(x * 32, y * 32, 32, 32, paintings_sprites, 1000)
                elif lines[y][x] == "2":
                    Paintings(x * 32, y * 32, 32, 32, paintings_sprites, 5000)
                elif lines[y][x] == "3":
                    Paintings(x * 32, y * 32, 32 * 2, 32 * 2, paintings_sprites, 50000)
                elif lines[y][x] == "d":
                    Wall(x * 32, y * 32, 32, 32, Exitdoors)
                elif lines[y][x] == "w":
                    Wall(x*32, y*32,32, 32, tiles1,"White")
                elif lines[y][x] == "E":
                    Wall(x * 32, y * 32, 32, 32, Exits, "Exitsign.png",True)
                if lines[y][x] == "K":
                    Key(x * 32, y * 32, 32, 32, paintings_sprites)
                if lines[y][x] == "D" and lines[y][x-1] == "D":
                    door=Door((x-1)*32, y*32, 32*2, 32, walls_sprites)
                current[x] = 0
        if width != 0:
            Wall((len(lines[0]) - width) * 32, (y - value) * 32, width * 32, value * 32, walls_sprites)
WIDTH_LIGHT = 30
MAX_DISTANCE = 100
FPS = 20

def calculate_angle(x1,y1,x2,y2):
    if x1 - x2 != 0:
        y = y1 - y2
        x = x1 - x2
        angle = math.degrees(math.atan(y / x))
        if x < 0 and y > 0 or x < 0 and y < 0:
            angle += 180
        return angle
    return None

def get_light(center, angle):
    pointlist = [center]
    hit_player = False
    for x in range(-1*WIDTH_LIGHT, WIDTH_LIGHT+1,2):
        current = angle + x
        hit = False
        targetposy = center[1] + (2 * math.sin(math.radians(current)) * MAX_DISTANCE)
        targetposx = center[0] + (2 * math.cos(math.radians(current)) * MAX_DISTANCE)
        xdisp = (targetposx - center[0]) / MAX_DISTANCE
        ydisp = (targetposy - center[1]) / MAX_DISTANCE
        for y in range(0,MAX_DISTANCE,2):
            for wall in renderlist:
                point = [center[0] + xdisp * y, center[1] + ydisp * y]
                if camera.apply(wall).collidepoint(point[0], point[1]):
                    pointlist.append(point)
                    hit = True
                    break
                if camera.apply(player2).collidepoint(point[0], point[1]):
                    pointlist.append(point)
                    hit = True
                    hit_player = True
                    break
            if hit:
                break
        if not hit:
            pointlist.append([targetposx, targetposy])

    if not hit_player:
        hit_player = False

    return pointlist, hit_player

def tilesrender():
    for tile in tiles1:
        if camera.apply(player2).colliderect(camera.apply(tile)):
            return True
    return False


def check_collisions():
    copy = player.rect.copy()
    copy2 = player.rect.copy()
    collidesx = False
    collidesy = False
    copy.x = position[0] + player.xvel - player.rect.width / 2
    copy2.y = position[1] + player.yvel - player.rect.height / 2
    for wall in renderlist:
        if camera.apply_rect(copy).colliderect(camera.apply(wall)):
            collidesx = True
            player.bouncex()
        if camera.apply_rect(copy2).colliderect(camera.apply(wall)):
            collidesy = True
            player.bouncey()
    if Exitdoors:
        for wall in Exitdoors:
            if camera.apply_rect(copy).colliderect(camera.apply(wall)):
                collidesx = True
                player.bouncex()
            if camera.apply_rect(copy2).colliderect(camera.apply(wall)):
                collidesy = True
                player.bouncey()

    if not collidesx:
        player.position[0] += player.xvel

    if not collidesy:
        player.position[1] += player.yvel

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

def create_render():
    changex = 0
    changey = 0
    targetposy1 = actual.y + (2 * math.sin(math.radians(targetangle + -1 * WIDTH_LIGHT)) * (MAX_DISTANCE + 20))
    targetposx1 = actual.x + (2 * math.cos(math.radians(targetangle + -1 * WIDTH_LIGHT)) * (MAX_DISTANCE + 20))
    targetposx2 = actual.x + (2 * math.cos(math.radians(targetangle + WIDTH_LIGHT)) * (MAX_DISTANCE + 20))
    targetposy2 = actual.y + (2 * math.sin(math.radians(targetangle + WIDTH_LIGHT)) * (MAX_DISTANCE + 20))
    maxx = max(targetposx1, targetposx2, actual.x)
    miny = min(targetposy1, targetposy2, actual.y)
    minx = min(targetposx1, targetposx2, actual.x)
    maxy = max(targetposy1, targetposy2, actual.y)
    diffx = maxx - minx
    diffy = maxy - miny
    return pygame.Rect(maxx + changex - MAX_DISTANCE*2, miny + changey, diffx,diffy)

def update_screen():
    # rendering for player 1
    for sprite in walls_sprites:
        if render.colliderect(camera.apply(sprite)) or renderwalls.colliderect(camera.apply(sprite)):
            renderlist.add(sprite)  # also have to add a second hitbox behind player so they can run into walls
        else:
            renderlist.remove(sprite)
    for painting in paintings_sprites:
        if render.colliderect(camera.apply(painting)) or renderwalls.colliderect(camera.apply(painting)):
            paintrenderlist.add(painting)
        else:
            paintrenderlist.remove(painting)

    # rendering for player 2
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

    sprites.update()
    sprites2.update()
    camera.update(player, WIDTH, HEIGHT)
    camera2.update(player2, WIDTH, HEIGHT)

def draw_screen():
    global health
    global seen
    screen.fill((255,255,255))
    box_surface_fill = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    player1surface.fill((0, 0, 0))
    player2surface.fill((123, 204, 128))
    pygame.draw.polygon(box_surface_fill, (255, 255, 100, max(0, min(brightness, 255))), pointlist)
    player1surface.blit(box_surface_fill, (0, 0))
    if Exitdoors:
        for tile in Exitdoors:
            player1surface.blit(tile.image, camera.apply(tile))
            player2surface.blit(tile.image, camera2.apply(tile))
    for tile in tiles1:
        player1surface.blit(tile.image, camera.apply(tile))
        player2surface.blit(tile.image, camera2.apply(tile))
    for sprite in sprites:
        player1surface.blit(sprite.image, camera.apply(sprite))
    for wall in renderlist:
        player1surface.blit(wall.image, camera.apply(wall))
    for painting in paintrenderlist:
        player1surface.blit(painting.image, camera.apply(painting))
    if battery>=10:
        for wall in renderlist_player2:
            player2surface.blit(wall.image,camera2.apply(wall))
        for painting in paintrenderlist_player2:
            player2surface.blit(painting.image,camera2.apply(painting))
            player2surface.blit(player2.image,camera2.apply(player2))
            player2surface.blit(player.image, camera2.apply(player))
    if battery<=0:
        player2surface.fill((0,0,0))
        player2surface.blit(Notification,(0,0))
    else:
        player2surface.blit(Night_vision, (-100, -100))
    for Exitss in Exits:
        player1surface.blit(Exitss.image, camera.apply(Exitss))
        player2surface.blit(Exitss.image, camera2.apply(Exitss))
    if flash_collide or tilesrender():
        if flash_collide:
            health-=.05
        player1surface.blit(player2.image, camera.apply(player2))#draw player on other side
        if seen!=True:
            seen=True
            pygame.mixer.music.play()

        if battery<=0:
            player2surface.blit(player2.image, camera2.apply(player2))
    box_surface_fill = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(box_surface_fill, (200, 255, 200, max(0, min(brightness, 255))), pointlist)
    player2surface.blit(box_surface_fill, (-camera.camera.x + camera2.camera.x, -camera.camera.y + camera2.camera.y))
    screen.blit(player2surface,(0,0))
    screen.blit(player1surface, (WIDTH//2, 0))

WIDTH = 1000
HEIGHT = 500

player1surface=pygame.Surface([WIDTH/2,HEIGHT])#Player 1 split screen side
player2surface=pygame.Surface([WIDTH/2,HEIGHT])#Player 2 split screen side
pygame.init()
pygame.mixer.init()
#Load assortment of images to be randomally put on paintings

pygame.mixer.music.load("Audio/Alert theme.mp3")

health=5
Notification=pygame.image.load("Graphics/Game Images/Notification.png")
Night_vision=pygame.transform.scale(pygame.image.load("Graphics/Game Images/Night Vision Scope.png"),(700,700))#Adds night vision effect
#Side note: Might need to be more transparent or blit images on top of this as painting frame colors are hard to see

screen = pygame.display.set_mode([WIDTH, HEIGHT])

walls = []
map = Map()
tiles1=pygame.sprite.Group()
Exits=pygame.sprite.Group()
Exitdoors=pygame.sprite.Group()
center = [WIDTH/2, HEIGHT/2]
mouse_position = center
sprites = pygame.sprite.Group()
renderlist = pygame.sprite.Group()
paintrenderlist=pygame.sprite.Group()
renderlist_player2= pygame.sprite.Group()
walls_sprites = pygame.sprite.Group()
paintings_sprites = pygame.sprite.Group()
paintrenderlist_player2=pygame.sprite.Group()
door = [0]
create_walls()

walls_sprites_player2 = walls_sprites.copy()
paintings_sprites_player2 = paintings_sprites.copy()
sprites2=pygame.sprite.Group()
player = Player([500,500], 20, 1)#use first two variables to change spawn position
sprites.add(player)
player2 = Player([700, 700], 20, 2)#same as above
sprites2.add(player2)
render = pygame.Rect(WIDTH/2 - MAX_DISTANCE * 2, HEIGHT/2 - MAX_DISTANCE * 2, MAX_DISTANCE * 4,MAX_DISTANCE * 4)
render2 = pygame.Rect((0,0),([WIDTH/2,HEIGHT]))
renderwalls=pygame.Rect(0, 0, 50,50)
camera = Camera(WIDTH, HEIGHT)
camera2 = Camera(WIDTH, HEIGHT)
targetangle = 260
crashed = False
brightness = 180
flash_collide = False
player2_score = 0
clock = pygame.time.Clock()
actual = camera.apply(player)
seen = False

font = pygame.font.SysFont(None,50)
battery=200
charging=False
Introscreen1=pygame.transform.scale(pygame.image.load("Graphics/Intro Images/Intro Screen.png"),(700,HEIGHT))
road=pygame.transform.scale(pygame.image.load("Graphics/Intro Images/Road.png"),(1000,HEIGHT))
car=pygame.transform.scale(pygame.image.load("Graphics/Intro Images/Car.png"),(100,100))
robberinstructions=pygame.image.load("Graphics/Intro Images/Robberslide1.png")
road2=road
button1=pygame.Rect((250,20),(450,HEIGHT-50))
Unclicked=True
while Unclicked:
    screen.fill((0,0,0))
    screen.blit(Introscreen1,(140,0))
    pygame.draw.rect(screen, (125, 124, 200), button1, 1)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button1.collidepoint(pygame.mouse.get_pos()):
                Unclicked=False
                for x in range(0,800,10):
                    screen.fill((0, 0, 0))
                    screen.blit(road, (600-x, 0))
                    screen.blit(road2, (600+200 - x, 0))
                    screen.blit(Introscreen1, (140-x, 0))
                    pygame.display.flip()

    pygame.display.flip()
Unclicked=True
disp=0
cardisp=0
cardispy=0
cardispconst=0.5
cardispconsty=0.5
slide=1
button=buttons(350,50,(0,0,0),"Click to continue",650,400,(255,255,255))

while Unclicked:

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.rect.collidepoint(pygame.mouse.get_pos()) and slide>4:
                Unclicked=False
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_SPACE or event.key==pygame.K_RIGHT:
                slide+=1
            if event.key==pygame.K_LEFT and slide>0:
                slide-=1
    if cardisp==-20 or cardisp== 20:
        cardispconst*=-1
    if cardispy==-10 or cardispy==10:
        cardispconsty*=-1
    cardisp+=cardispconst
    cardispy+=cardispconsty
    disp+=5
    if disp>=1000:
        disp=0
    screen.fill((0, 0, 0))
    screen.blit(road, (0-disp, 0))
    screen.blit(road2, (0+1000 - disp, 0))
    screen.blit(car,(WIDTH//2-cardisp,HEIGHT//2+100-cardispy))
    if slide==1:
        robberinstructions=pygame.image.load("Graphics/Intro Images/Robberslide1.png")
    elif slide==2:
        robberinstructions=pygame.image.load("Graphics/Intro Images/Robberslide2.png")
    elif slide==3:
        robberinstructions=pygame.image.load("Graphics/Intro Images/Robberslide3.png")
    elif slide==4:
        robberinstructions=pygame.image.load("Graphics/Intro Images/Robberslide4.png")
    else:
        screen.blit(button.surface,(button.x,button.y))
    screen.blit(robberinstructions,(0,0))
    pygame.display.flip()
Unclicked=True
Guardinstructions=pygame.image.load("Graphics/Intro Images/Guardinstructions.png")
button=buttons(180,50,(255,255,0),"Click to continue",350,450,(0,0,0),"Arial",28)
while Unclicked:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                Unclicked=False
    screen.fill((255,255,255))
    screen.blit(Guardinstructions,(0,0))
    screen.blit(button.surface,(button.x,button.y))
    pygame.display.flip()


win=False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEMOTION:
            mouse_position = event.pos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                charging=True
            elif charging!=True:
                if event.key == pygame.K_SPACE:
                    for painting in paintrenderlist_player2:
                        if camera2.apply(player2).colliderect(camera2.apply(painting)):
                            paintings_sprites_player2.remove(painting)
                            paintrenderlist_player2.remove(painting)
                            paintings_sprites.remove(painting)
                            paintrenderlist.remove(painting)
                            player2_score += painting.points
                            if painting.points == 0:
                                key_obtained = True
                                print("bruh")
                                door.rect.x=1000000
                            break

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                charging=False


    player.move(pygame.key.get_pressed(), 2)
    if not charging:
        player2.move(pygame.key.get_pressed(), 1)

    #Doesnt matter
    position = player.get_position()
    position2 = player2.get_position()
    actual = camera.apply(player)
    new_angle = calculate_angle(mouse_position[0], mouse_position[1], actual.x + player.width+WIDTH//2, actual.y + player.width)
    if new_angle:
        targetangle = new_angle

    player.rotate(-targetangle)
    render = create_render()
    actual2 = camera2.apply(player2)
    render2.center = [WIDTH//4,HEIGHT//2]
    pointlist,flash_collide = get_light([actual.x + player.width // 2, actual.y + player.width // 2], targetangle)
    renderwalls.center=[actual.x+10,actual.y+10]
    check_collisions()
    check_collisions2()
    #---------------------------------------
    draw_screen()
    update_screen()
    clock.tick(FPS)
    if battery>0:
        battery-=0.5
    if charging and battery<200:
        battery += 1.5
    if battery>20:
        night_vision_counter = font.render(str(round(((battery/200)*100)))+"% Charge", True, (255,255,255), (0, 0, 0))
    else:
        night_vision_counter = font.render(str(round(((battery / 200) * 100))) + "% Charge", True, (255, 0, 0),
                                           (0, 0, 0))
    screen.blit(night_vision_counter, (0, 0))
    if player2_score>=20000:
        Exitdoors=None
        if player2.get_position()[0]<=0:
            win=True#put win here
            crashed=True
    if health<=0:
        crashed=True
    pygame.display.flip()

done=False
font1 = pygame.font.SysFont("Arial", 60)
font2 = pygame.font.SysFont("Arial", 80)
WIDTH=500
HEIGHT=500
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    if win==True:
        robberwin()
    else:
        guardwin()
    printscore()
    generate_text("Game over",(WIDTH / 2, HEIGHT / 3),(0,125,0),font2)
    pygame.display.flip()