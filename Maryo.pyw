import pygame, sys, os, random, pausemenu
from time import sleep
from pygame.locals import *


pygame.init()

pygame.mouse.set_visible(1)

root_dir = os.path.join(os.path.dirname(sys.argv[0]), 'Sprites') #Sprites file path

stat = 'New game started'   

window_height = 700
window_width = int((12 / 7) * window_height)       #To maintain an aspect ratio. 

check = 0       #Variable to detect hits.
level = 0
fps = 60

transformation_ratio = window_height/700   #Scale speed according to size of window.
    
addnewflamerate = 20
playerflamerate = 30

shootflag = 0   #Flag which tells if ammo has been replenished.


volumeaction = 'mute'           #Variable for volume control.


white  = (255,255,255)
blue   = (0,0,255)
black  = (0,0,0)
green  = (0,255,0)
red    = (255,0,0)
yellow = (255,255,0)


class dragon( pygame.sprite.Sprite):

    global firerect,rect,Canvas
    up=False
    down=True
    velocity = 10 * transformation_ratio

    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(root_dir, 'dragon.png'))
        self.image.set_colorkey(black)
        self.image = pygame.transform.scale( self.image, ( int(100*(window_width/1200)), int(86*(window_height/700)) ) ).convert()
        self.mask  = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.right = window_width
        self.rect.top = window_height/2

    def update(self):

        if(self.rect.top < cactusrect.bottom):
            self.up = False
            self.down = True

        if(self.rect.bottom > firerect.top):
            self.down = False
            self.up = True

        if(self.down):
            self.rect.bottom += dragon.velocity

        if(self.up):
            self.rect.top -= dragon.velocity

        Canvas.blit(self.image,self.rect)

    def return_height(self):

        return(self.rect.top)
    
    def return_side(self):

        return((self.rect.left,self.rect.right))
        


class flames(pygame.sprite.Sprite):

    def __init__(self,opt):
        self.opt = opt;
        pygame.sprite.Sprite.__init__(self)
        if opt == 0:
            flames.flamespeed = 20 * transformation_ratio
            self.image = pygame.image.load(os.path.join(root_dir, 'fireball.png'))
            self.image.set_colorkey(black)
            self.image = pygame.transform.scale( self.image, ( int(40*(window_width/1200)), int(26*(window_height/700)) ) ).convert()
            self.mask  = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.top = Dragon.return_height()
            self.rect.right = Dragon.rect.left

        if opt == 1:
            flames.bluflamespeed = 50 * transformation_ratio
            self.image = pygame.image.load(os.path.join(root_dir, 'marflm.png'))
            self.image.set_colorkey(white)
            self.image = pygame.transform.scale( self.image, ( int(40*0.5*(window_width/1200)), int(26*0.5*(window_height/700)) ) ).convert()
            self.mask  = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.top = player.rect.centery
            self.rect.left = player.rect.right
        
    def update(self):
        if self.rect.top < cactusrect.bottom:
            self.rect.top = cactusrect.bottom
        if self.opt == 0:
            self.rect.left -= flames.flamespeed
        if self.opt == 1:
            self.rect.right += flames.bluflamespeed
    
    def collision(self):

        if(self.rect.left == 0 or self.rect.right >= window_width):
            return(True)
        else:
            return(False)

class maryo(pygame.sprite.Sprite):

    global moveup, movedown, gravity, moveright, moveleft, cactusrect, firerect

    speed = 10 * transformation_ratio
    upspeed = 20 * transformation_ratio
    acc_due_to_gravity = 5 * transformation_ratio
    

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.image = pygame.image.load(os.path.join(root_dir, 'Maryo.png'))
        self.image.set_colorkey(white)
        self.image = pygame.transform.scale( self.image, ( int(50*(window_width/1200)), int(63*(window_height/700)) ) ).convert()
        self.mask  = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.top = window_height/2
        self.rect.left = (1/35)*window_height
        

    def update(self):

        if(moveup and (self.rect.top > cactusrect.bottom)):
            self.score += 1
            self.rect.top -= maryo.upspeed

        if(movedown and (self.rect.bottom < firerect.top)):
            self.score += 1
            self.rect.bottom += maryo.speed

        if(gravity and (self.rect.bottom < firerect.top)):
            self.rect.bottom += maryo.acc_due_to_gravity

        if(moveright and (self.rect.right < Dragon.rect.left)):
            self.rect.right += maryo.speed

        if(moveleft and (self.rect.left > 0)):
            self.rect.right -= maryo.speed

class life(pygame.sprite.Sprite):
    
    lifebox_w = (9/20)*window_width
    lifebox_h = (3/70)*window_height
    

    def __init__(self, holder):

        self.Life = 100
        self.damage = 0
        self.lifeof = holder
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((life.lifebox_w, life.lifebox_h)).convert()
        self.image.fill(red)
        self.rect = self.image.get_rect()

        if self.lifeof.__class__.__name__ == 'maryo':
            self.rect.x, self.rect.y = window_width/60, window_width/70
            self.mould = (0, life.lifebox_h), (0, 0), (life.lifebox_w, 0), ((0.9)*life.lifebox_w, life.lifebox_h)
            pygame.draw.polygon(self.image, white, (self.mould[2], (life.lifebox_w, life.lifebox_h), self.mould[3]))
            

        if self.lifeof.__class__.__name__ == 'dragon':
            self.rect.right, self.rect.y = window_width*(59/60), window_width/70
            self.mould = (life.lifebox_w, life.lifebox_h), (life.lifebox_w, 0), (0 ,0), ((0.1)*life.lifebox_w, life.lifebox_h)
            pygame.draw.polygon(self.image, white, (self.mould[2], (0, life.lifebox_h), self.mould[3]))

        self.border = self.image.get_rect()
        
    
    def update(self):

        if stat == 'lost' and self.lifeof.__class__.__name__ == 'maryo':

            self.image.fill(white)

        else:

            flamehits(self.lifeof)
                

            self.image.fill(white)
            
            if self.lifeof.__class__.__name__ == 'maryo':

                if self.damage != 0:
                
                    self.border.left += life.lifebox_w/10

                self.Life -= self.damage

                self.damage = 0

                self.image.fill(red, self.border) 
                pygame.draw.polygon(self.image, white, (self.mould[2], (life.lifebox_w, life.lifebox_h), self.mould[3]))
                
            if self.lifeof.__class__.__name__ == 'dragon':

                if self.damage != 0:
                
                    self.border.width -= life.lifebox_w/10

                self.Life -= self.damage

                self.damage = 0

                self.image.fill(red, self.border)
                pygame.draw.polygon(self.image, white, (self.mould[2], (0, life.lifebox_h), self.mould[3]))

        pygame.draw.polygon(self.image, green, self.mould,int(5 * transformation_ratio))
        

class power(pygame.sprite.Sprite):

    pwrbar_w = (3/8)*window_width
    pwrbar_h = (3/140)*window_height
    

    def __init__(self):

        self.Power = 0
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((power.pwrbar_w, power.pwrbar_h)).convert()
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = window_width/60, (11/140)*window_height

    def update(self):

        if shootflag == 0 :
            self.image.fill(black)
        else :
            self.image.fill(blue)


def terminate():
    pygame.quit()
    sys.exit()


def waitforkey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


def flamehits(Object):
    
    global check

    if Object.__class__.__name__ == 'dragon':
        List = thndrboltlist
        for l in List:
            if(pygame.sprite.collide_mask(Object,l) != None):
                if volumeaction != 'muted':
                    drghit.play()
                thndrboltlist.remove(l)
                dragon_life.damage = 10
                check =1
                
    elif Object.__class__.__name__ == 'maryo':
        List = flamelist
        for l in List:
            if(pygame.sprite.collide_mask(Object,l) != None):
                if volumeaction != 'muted':
                    plrhit.play()
                sleep(0.2)
                flamelist.remove(l)
                maryo_life.damage = 10
                check =1
    return check


def drawtext(text,font,surface,x,y,colour = white):
    textobj = font.render(text,1,colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)


def check_level(score):
    
    global window_height, level, cactusrect, firerect

    if score in range(0,250) and level != 1:
        level = 1
        cactusrect.bottom += window_height*(1/7)*(1/4)
        firerect.top -= window_height*(1/7)*(1/4)
            
    elif score in range(250,500) and level != 2:
        level=2
        cactusrect.bottom += window_height*(1/7)*(1/4)
        firerect.top -= window_height*(1/7)*(1/4)
        
    elif score in range(500,750) and level != 3:
        level=3
        cactusrect.bottom += window_height*(1/7)*(1/4)
        firerect.top -= window_height*(1/7)*(1/4)
        
    elif score in range(750,1000) and level != 4:
        level=4
        cactusrect.bottom += window_height*(1/7)*(1/4)
        firerect.top -= window_height*(1/7)*(1/4)
    

mainClock = pygame.time.Clock()

pygame.display.set_caption('Maryo')
Canvas = pygame.display.set_mode((window_width,window_height))#,pygame.FULLSCREEN)

scorefont = pygame.font.SysFont(None, int((1/28)*window_height), False, False)
txtfont = pygame.font.SysFont('Copperplate Gothic', int((3/140)*window_height), True, True)

fireimage = pygame.image.load(os.path.join(root_dir, 'fire_bricks.png'))
fireimage = pygame.transform.scale( fireimage, ( int(1200*(window_width/1200)), int(200*(window_height/700)) ) )
firerect = fireimage.get_rect()
firerect.top = window_height*(13/14)

cactusimage = pygame.image.load(os.path.join(root_dir, 'cactus_bricks.png'))
cactusimage = pygame.transform.scale( cactusimage, ( int(1200*(window_width/1200)), int(200*(window_height/700)) ) )
cactusrect = cactusimage.get_rect()
cactusrect.bottom = window_height*(5/28)

subsurface = Canvas.subsurface((0,0,window_width,(3/28)*window_height))


startimage = pygame.image.load(os.path.join(root_dir, 'start.png'))
startimage = pygame.transform.scale( startimage, ( int(518*(window_width/1200)), int(276*(window_height/700)) ) )
startimagerect = startimage.get_rect()
startimagerect.centerx = window_width/2
startimagerect.centery = window_height/2

endimage = pygame.image.load(os.path.join(root_dir, 'end.png'))
endimage = pygame.transform.scale( endimage, ( int(519*(window_width/1200)), int(277*(window_height/700)) ) )
endimage.set_alpha(140)
endimagerect = endimage.get_rect()
endimagerect.centerx = window_width/2
endimagerect.centery = window_height*(4/7)

endwinimage = pygame.image.load(os.path.join(root_dir, 'endwin.png'))
endwinimage = pygame.transform.scale( endwinimage, ( int(519*(window_width/1200)), int(277*(window_height/700)) ) )
endwinimage.set_alpha(140)
endwinimagerect = endwinimage.get_rect()
endwinimagerect.centerx = window_width/2
endwinimagerect.centery = window_height*(4/7)
       
pygame.mixer.music.load(os.path.join(root_dir, 'mario_theme.wav'))
gameoversound = pygame.mixer.Sound(os.path.join(root_dir, 'mario_dies.wav'))
shot_fired = pygame.mixer.Sound(os.path.join(root_dir, 'Shot_Fired.wav'))
dry_fire = pygame.mixer.Sound(os.path.join(root_dir, 'Dry_Fire.wav'))
plrhit = pygame.mixer.Sound(os.path.join(root_dir, 'fireatk.wav'))
drghit = pygame.mixer.Sound(os.path.join(root_dir, 'draghit.wav'))


Canvas.fill(black)
Canvas.blit(startimage, startimagerect)

pygame.display.flip()

waitforkey()

topscore = 0

allsprites = pygame.sprite.Group()
flamelist = pygame.sprite.Group()
thndrboltlist = pygame.sprite.Group()

while True:
    
    flamelist.empty()
    thndrboltlist.empty()
    allsprites.empty()

    Dragon = dragon()
    allsprites.add(Dragon)

    player = maryo()
    allsprites.add(player)

    dragon_life = life(Dragon)
    maryo_life = life(player)
    allsprites.add(dragon_life, maryo_life)

    Power = power()
    allsprites.add(Power)

    moveup = movedown = moveright = moveleft = False
    gravity         = True
    count           = 0
    flameaddcounter = 0
    check           = 0
    level           = 0
    stat            = 'null'

    firerect.top = window_height*(13/14)
    cactusrect.bottom = window_height*(5/28)

    gameoversound.stop()

    if volumeaction != 'muted':
        pygame.mixer.music.play(-1,0.0)

    
   

    while (stat != 'lost' and stat != 'won'):
        shootflag = 0
        count+=1
        if count >= playerflamerate:
            shootflag = 1

        moveup    = pygame.key.get_pressed()[pygame.K_UP]
        movedown  = pygame.key.get_pressed()[pygame.K_DOWN]
        moveleft  = pygame.key.get_pressed()[pygame.K_LEFT]
        moveright = pygame.key.get_pressed()[pygame.K_RIGHT]

        if moveup and movedown:
            moveup = False
            movedown = False

        for event in pygame.event.get():


            if event.type == QUIT:
                terminate()
                

            if event.type == KEYDOWN:

                '''stat prevents opening of pause menu and player's firing at the starting and ending screen of the game.'''
                
                if event.key == K_LCTRL and stat=='null' :
                    volumeaction = pausemenu.pausemenu(Canvas, window_height, window_width)
                
                if event.key == K_SPACE and stat == 'null' and count >= playerflamerate :
                    if volumeaction != 'muted':
                        shot_fired.play()
                    player_flame = flames(1)
                    thndrboltlist.add(player_flame)
                    count = 0
                elif event.key == K_SPACE:
                    if volumeaction != 'muted':
                        dry_fire.play()
                stat = 'null'
                    

            if event.type == KEYUP:
                    
                if event.key == K_ESCAPE:
                    terminate()
                    
        flameaddcounter += 1
        check_level(player.score)

        if flameaddcounter == addnewflamerate:
            
            addnewflamerate = random.randint(10,20)
            flameaddcounter = 0
            newflame = flames(0)
            flamelist.add(newflame)

        for f in flamelist:
            if(f.collision()):
                flamelist.remove(f)

        for t in thndrboltlist:
            if(t.collision()):
                thndrboltlist.remove(t)
                
        allsprites.update()
        

        if maryo_life.Life <= 0:
            
            stat = 'lost'

        if dragon_life.Life <= 0:

                stat = 'won'
            

        if (player.rect.bottom >= firerect.top) or (player.rect.top <= cactusrect.bottom):
            
            maryo_life.Life = 0
            stat = 'lost'
            maryo_life.update()
            
        if stat != 'lost':
            for f in flamelist:
                f.update()
            for t in thndrboltlist:
                t.update()

        Canvas.fill(black)
        Canvas.blit(fireimage,firerect)
        Canvas.blit(cactusimage,cactusrect)
        subsurface.fill(white)
        allsprites.draw(Canvas)
        flamelist.draw(Canvas)
        thndrboltlist.draw(Canvas)

        drawtext('VS',pygame.font.SysFont('Algerian', int((11/140)*window_height), True, False),subsurface,window_width/2.13,subsurface.get_height()/4.2,green)
        drawtext('Score : %s | Top score : %s | Level : %s' %(player.score, topscore, level),scorefont,Canvas,(0.4)*window_width, cactusrect.bottom + window_height/70)
        if stat == 'lost':
            if player.score > topscore:
                topscore = player.score 
        else:
            drawtext('PRESS LEFT CTRL TO PAUSE', txtfont, Canvas, (0.4)*window_width, cactusrect.bottom + window_height/20, white)


        pygame.display.flip()

        mainClock.tick_busy_loop(30)



    pygame.mixer.music.stop()

    if volumeaction != 'muted':
        gameoversound.play()

    if stat == 'won':
        Canvas.blit(endwinimage,endwinimagerect)
    else:
        Canvas.blit(endimage, endimagerect)
    pygame.display.update()
    
    waitforkey()
    sleep(1)


            
                    

            



    

        

        
        
