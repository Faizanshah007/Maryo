import pygame,sys,random
from pygame.locals import *
from cmath import *

volumeaction = 'mute'

def pausemenu(Canvas, window_height, window_width):
    
    global volumeaction

    pwindow_height = 2/7 * window_width
    pwindow_width = 3/4 * pwindow_height

    optrect_width = pwindow_width*(2/3)
    optrect_height = pwindow_height/8

    txtshiftx = optrect_width/4
    txtshifty = optrect_height/5

    margin = pwindow_width/6
    rectspacing = pwindow_height/20
    titlespacing = (3/8)*pwindow_height

    white = (255,255,255)
    blue  = (0,0,255)
    green = (0,255,0)

    pygame.mouse.set_visible(1)

    pos = -1

    position = stickmouse = (-1,-1)

    pfont=pygame.font.SysFont('Comic Sans MS', 30, True, False)
    optfont=pygame.font.SysFont('Century Gothic', 25, True, True)

    def interact(x,y,s,Pos):

        if ((rectb.left<=x and rectb.right>=x and rectb.top<=y and rectb.bottom>=y)and Pos <= -1) or Pos == 0:

            pygame.draw.rect(Canvas,white,(rectb.left-5,rectb.top-5,rectb.width+10,rectb.height+10),3)
                
            if s == True:
                return('Resume')
            if s == False:
                return('Paused')
                

        elif ((rectc.left<=x and rectc.right>=x and rectc.top<=y and rectc.bottom>=y) and Pos <= -1) or Pos == 1:

            pygame.draw.rect(Canvas,white,(rectc.left-5,rectc.top-5,rectc.width+10,rectc.height+10),3)
                
            if s == True:
                return('Mute/Unmute')
            if s == False:
                return('NoChange')


        elif ((rectd.left<=x and rectd.right>=x and rectd.top<=y and rectd.bottom>=y) and Pos <= -1) or Pos == 2:

            pygame.draw.rect(Canvas,white,(rectd.left-5,rectd.top-5,rectd.width+10,rectd.height+10),3)

                
            if s == True:
                pygame.quit()
                sys.exit()
            if s == False:
                return('NoExit')

        else:
            return('Outside')  #special value

    while True:
        
        recta = pygame.draw.rect(Canvas, green, ((1.13*window_width/2.2)-(pwindow_width/2),(window_height/1.8)-(pwindow_height/2), pwindow_width, pwindow_height), 0)

        pygame.draw.rect(Canvas, blue, recta, 10)

        rectb = pygame.draw.rect(Canvas, white, (recta.left+margin, recta.top+titlespacing+rectspacing, optrect_width, optrect_height), 3)

        rectc = pygame.draw.rect(Canvas, white, (rectb.left, rectb.height+rectb.top+rectspacing, optrect_width, optrect_height), 3)

        rectd = pygame.draw.rect(Canvas, white, (rectc.left, rectc.height+rectc.top+rectspacing, optrect_width, optrect_height), 3)


        Canvas.blit(pfont.render('PAUSE MENU', 1, white), (rectd.left, rectb.top-pwindow_height/4))

        Canvas.blit(optfont.render('Resume', 1, white), (rectb.left+txtshiftx, rectb.top+txtshifty))

        if volumeaction == 'mute':
            Canvas.blit(optfont.render('Mute', 1, white), (rectc.left+txtshiftx, rectc.top+txtshifty))

        if volumeaction == 'muted':
            Canvas.blit(optfont.render('Unmute', 1, white), (rectc.left+txtshiftx, rectc.top+txtshifty))

        Canvas.blit(optfont.render('Exit', 1, white), (rectd.left+txtshiftx, rectd.top+txtshifty))


            
        for event in pygame.event.get():

            Action = ''

            keypressed = False

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEMOTION:
                if pos >= 0:
                    pos = -1
                position = pygame.mouse.get_pos()
                if pygame.event.peek(K_RETURN):
                    keypressed = True

            if pos<= -1:
                keypressed = pygame.mouse.get_pressed()[0]

                
            if event.type == KEYDOWN:

         
                if event.key == K_ESCAPE:

                    pygame.quit()
                    sys.exit()

                if event.key == K_UP :

                    if pos == 10:
                        pos = 0
                    

                    elif pos > -1:
                        pos -=1

                        if pos < 0:
                            pos = 2

                    else :
                        if pos == -1:
                            pos = 2
                            
                        else:
                            pos = abs(pos)%2 # -1_2 -2_0 -3_1
                
                if event.key == K_DOWN :

                    if pos == 10:
                        pos = 0

                    

                    elif pos > -1:
                        pos +=1

                        if pos > 2:
                            pos = 0

                    else :
                        pos = abs(pos)%3 #change for 4    -1_1  -2_2 -3_0


                if event.key == K_RETURN :

                    keypressed = True
                    

            Action=interact(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], keypressed, pos)


            if Action == 'Outside':

                pos = 10
                
                
            if Action == 'Resume':
                
                pygame.mouse.set_visible(0)
                return volumeaction
            
            
            if Action == 'Mute/Unmute':
                    
                if volumeaction == 'mute':
                    pygame.mixer.music.pause()
                    volumeaction = 'muted'
    
                elif volumeaction == 'muted':
                    
                    pygame.mixer.music.play()
                    volumeaction = 'mute'


            if Action == 'Paused':
                
                if pos <= -1:
                    pos = -1

                    
            if Action == 'NoChange':
                                
                if pos <= -1:
                    pos = -2
                    
                
            if Action == 'NoExit':

                if pos <= -1:
                    pos = -3
                    
                
            pygame.display.update();
    
