import pygame
import random

class Enemy:
    def __init__(self, game, x,y=True):
        self.game = game
        self.x = x
        self.y = y
        self.speed = 2
        self.size = (40, 40)
        self.remove = False
        if y == True:
            self.y = random.randint(10, 334)
        self.choose_enemy()


    def choose_enemy(self):
        number = random.randint(1,2)
        self.animation = self.game.assets[f'enemy{number}/run'].copy()
        self.animation.frame = random.randint(0,7)

    def rect(self):
        return pygame.rect.Rect(self.x+10, self.y+5, self.size[0]-20, self.size[1]-10)

    def update(self):
        self.x -= 3
        if self.x < -50:
            self.remove = True
        self.animation.update()

    def render(self):
        self.game.display.blit(self.animation.img(), (self.x, self.y))
        #pygame.draw.rect(self.game.display, (0,0,0), self.rect())
