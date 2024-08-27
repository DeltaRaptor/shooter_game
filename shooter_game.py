#Создай собственный Шутер!
from time import *
from pygame import *
from random import *
import os
init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.name = player_image
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def dvizenie(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 625:
            self.rect.x += self.speed
            
        if keys_pressed[K_a] and self.rect.x > 0:
                self.rect.x -= self.speed
    def babah(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w]:
            builets.add(AnigilatornayaPyshka('bullet.png', self.rect.x, self.rect.y, 10))
            for i in builets:
                i.image = transform.scale(image.load('bullet.png'), (10, 10)) 

class Enemy(GameSprite):
    def update(self):
        if self.rect.y < 550:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(0,650)
            if self.name == 'ufo.png':
                global propysk
                propysk += 1

class AnigilatornayaPyshka(GameSprite):    
    def update(self):
        if self.rect.y > 0:
            self.rect.y -= self.speed
            dead_note = sprite.groupcollide(builets, monster, True, True)
            dead_note2 = sprite.spritecollideany(raketa_gagarina, kamni)
            for i in dead_note:
                global ybito
                ybito += 1
            if dead_note2:
                global stolknovenie
                stolknovenie == True
        else:
            self.kill()
            
stolknovenie = False        

monster = sprite.Group()
builets = sprite.Group()
kamni = sprite.Group()

propysk = 0
ybito = 0
for i in range(5):
    monster.add(Enemy('ufo.png', randint(0,650),-60, randint(2,5)))
for i in range(3):
    kamni.add(Enemy('asteroid.png', randint(0,650),-60, randint(2,5)))

raketa_gagarina = Player('rocket.png', 300, 400, 5)
NLO1 = Enemy('ufo.png', randint(0,650),-60, 3)       

window = display.set_mode((700, 500))
galaxy = transform.scale(image.load('galaxy.jpg'), (700, 500))

clock = time.Clock()

font.init()
font1 = font.Font(None, 36)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

game = True

while game == True and propysk < 3 and ybito < 5:
    for e in event.get():
        if e.type == QUIT:
            game = False
    window.blit(galaxy, (0,0))
    text_lose = font1.render('Пропущено: '+ str(propysk), True, (200, 200, 200))
    text_win = font1.render('Прибито: '+ str(ybito), True, (200, 200, 200))
    window.blit(text_lose, (0,470))
    window.blit(text_win, (0,440))
    raketa_gagarina.reset()
    raketa_gagarina.dvizenie()
    monster.draw(window)
    builets.draw(window)
    kamni.draw(window)
    monster.update()
    builets.update()
    kamni.update()
    raketa_gagarina.babah()
    clock.tick(60)
    display.update()

if propysk >= 3 or stolknovenie == True:
    end = font1.render('You Died! [idiot]' , True, (200, 0, 0))
if ybito >= 5:
    end = font1.render('Победа!', True, (0, 200, 0))

while game == True:
    for e in event.get():
        if e.type == QUIT:
            game = False
    window.blit(end, (290,200))
    clock.tick(60)
    display.update()