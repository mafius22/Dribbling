import pygame
import random

class Enemy:
    def __init__(self, game, x, y, number):
        self.game = game
        self.number = number
        self.startingY = y
        self.x = x
        self.y = y
        self.normalSpeed = 3
        self.speed = self.normalSpeed
        self.speedy = self.normalSpeed
        self.size = (40, 40)
        self.remove = False
        if y == True:
            self.y = random.randint(10, 334)
        self.choose_enemy()


    def choose_enemy(self):
        self.animation = self.game.assets[f'enemy{random.randint(0,1)}/run'].copy()
        self.animation.frame = random.randint(0,7)

    def rect(self):
        return pygame.rect.Rect(self.x+10, self.y+5, self.size[0]-20, self.size[1]-10)

    def update(self):
        self.x -= self.speed
        if self.x < -50:
            self.remove = True

        if self.number == 1:
            self.y += self.speedy
            if self.y < self.startingY - 100:
                self.speedy *= -1
            elif self.y > self.startingY + 100 - 40:
                self.speedy *= -1

        self.animation.update()

    def render(self):
        self.game.display.blit(self.animation.img(), (self.x, self.y))
        #pygame.draw.rect(self.game.display, (0,0,0), self.rect())
