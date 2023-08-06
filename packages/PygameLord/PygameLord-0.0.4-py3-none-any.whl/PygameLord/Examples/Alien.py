#LordLynx
#Part of PygameLord
import PygameLord
from PygameLord.ColorConstants import*
import pygame
from pygame.locals import*
import random
import time
import sys
pygame.init()
WINDOW_WIDTH = 360
WINDOW_HIGHT = 500
Screen =  pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HIGHT),0, 32)
Aliens = PygameLord.Images.Tilesheet('./Images/Aliens.png',(32,32))
Barier = PygameLord.Images.Tilesheet('./Images/Barrier.png',(32,32))
Player = pygame.image.load('./Images/Player.png')
Player_Lazer = pygame.image.load('./Images/Player_Bolt.png')
Alien_Lazer = pygame.image.load('./Images/Alien_Bolt.png')
Lazer_Sound = pygame.mixer.Sound('./Sounds/Lazer.wav')
Explotion_Sound = pygame.mixer.Sound('./Sounds/Boom.wav')
pygame.mixer.music.load('./Sounds/Assistance.mp3')
pygame.mixer.music.play(-1, 0.0)
world = []
font = pygame.font.SysFont(None, 24)
TEXTCOLOR = AO
pygame.display.set_caption('Alien')
fps = 20
Clock = pygame.time.Clock()
class game:
    def __init__(self, x1boundary,x2boundary, y1boundary,y2boundary):
        self.x1 = x1boundary
        self.x2 = x2boundary
        self.y1 = y1boundary
        self.y2 = y2boundary
        self.level = 0
        self.to_level = 100
        self.score = 0
        self.to_score = 100
        self.objects = []
        self.direction = 32
        self.lives = 3
    def run(self,fps):
        PygameLord.Font.display_text(('score\t'+str(self.score) +'\nlevel\t'+ str(self.level) + '\nlives\t' + str(self.lives)),None,Screen,16,0,TEXTCOLOR)
        if self.score == self.to_level:
            self.to_level += self.to_score
            self.level += 1
            self.lives += 1
        if self.lives == 0:
            PygameLord.exit()
            sys.exit()
        d = []
        for i in self.objects:
            i.run(self)
        for i in self.objects:
            if i.kind == 'A':
                d.append(i)
                if i.x == self.y2:
                    self.direction = -32

                if i.x == self.y1:
                    self.direction = 32
        if d == []:
            generate()
        fps += self.level
        
class lazer:
    def __init__(self,x,y,im,di,kind):
        self.x =x
        self.y = y
        self.move = 0
        self.im = im
        self.kind = kind
        self.di = di

    def run(self, game):
        self.speed = 2
        self.move += 1
        if self.move == self.speed:
            self.y += self.di
            self.move = 0
            if self. di == 32:
                if self.y == game.y1:
                    game.objects.remove(self)
            else:
                if self.y == game.y2:
                    game.objects.remove(self)              
        Screen.blit(self.im,pygame.Rect(self.x,self.y,32,32))
        
class wall:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.health = 4
        self.sheet = Barier
        self.kind = 'W'
    def run(self,game):
        self.rect = (self.x,self.y,32,32)
        Screen.blit(self.sheet.Get_Tile((self.health,0)),self.rect)                    
        for w in game.objects:
            if w.x == self.x and w.y == self.y and w.kind == 'AL'  :
                game.objects.remove(w)
                Explotion_Sound.play()
                self.health -= 1
            if self.health == -1:
                try:
                    game.objects.remove(self)
                    #
                except:
                    pass
        

class player:
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.move = 0
        self.f = 0
        self.kind = 'P'
        
    def shoot(self,game):
        game.objects.append(lazer(self.x,self.y,Player_Lazer,-32,'PL'))
        
    def run(self, game,):
        for w in game.objects:
            if w.x == self.x and w.y == self.y and w.kind == 'AL':
                game.objects.remove(w)
                game.lives -= 1
                Explotion_Sound.play()
        for event in pygame.event.get():
            if event.type == QUIT:
                PygameLord.quit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.x -= 32
                    if self. x == game.x1:
                        self.x += 32
                if event.key == K_RIGHT:
                    self.x += 32
                    if self. x == game.x2:
                        self.x -= 32
                if event.key == K_SPACE:
                    Lazer_Sound.play()
                    self.shoot(game)
        self.rect = (self.x,self.y,32,32)
        Screen.blit(Player,self.rect)        


class alien:
    def __init__(self,x,y):
        self.x =x
        self.y =y
        self.count = 0
        self.frame = 0
        self.sheet =  Aliens
        self.kind = 'A'
        self.Pass = 0
        self.downspeed = 16
    def shoot(self,game):
        Lazer_Sound.play()
        game.objects.append(lazer(self.x,self.y,Alien_Lazer,32, 'AL'))
    def run(self,game):
        for w in game.objects:
            if w.x == self.x and w.y == self.y and w.kind == 'PL':
                game.objects.remove(self)
                game.objects.remove(w)
                game.score += 10
                Explotion_Sound.play()
        self.speed = 10#=abs(10- game.level *5)
        self.count += 1
        if self.count == self.speed:
            self.x += game.direction
            self.count = 0
            self.Pass += 1
            if self.Pass == self.downspeed:
                self.y += 32
                self.Pass = 0
        if self.frame == 0:
            self.frame = 1
        else:
            self.frame = 0
        if  random.randint(1,1000) == 1:
            self.shoot(game)
        if self.y == game.x2-64:
            Explotion_Sound.play()
            time.sleep(3)
            PygameLord.exit()
            sys.exit()
        self.rect = (self.x,self.y,32,32)
        Screen.blit(self.sheet.Get_Tile((self.frame,0)),self.rect)

        
s = game(32,320,0,320)
p = player (64,320)
s.objects.append(p)
def generate():
    d = wall(64,320-64)
    s.objects.append(d)
    d = wall(160,320-64)
    s.objects.append(d)
    d = wall(256,320-64)
    s.objects.append(d)
    for x in range (1,6):
        for y in range (2,6):
            s.objects.append( alien(x*32,y*32))
generate()  
while True:
    Screen.fill(WHITE)
    s.run(fps)
    Clock.tick(fps)
    pygame.display.update()










