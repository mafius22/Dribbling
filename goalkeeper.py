import pygame
import random

class Goalkeeper:
    def __init__(self, game):
        self.game = game
        self.x = self.game.display.width - 40 + 72 + 120
        self.y = self.game.display.height//2
        self.normalSpeed = 2
        self.image = self.game.assets['goalkeeper']
        self.speed = self.normalSpeed
        self.size = (40, 40)
        self.move = False

    def reset(self):
        self.move = False
        self.x = self.game.display.width - 40 + 72 + 120
        self.y = self.game.display.height // 2

    def rect(self):
        return pygame.rect.Rect(self.x+10, self.y+5, self.size[0]-20, self.size[1]-10)

    def update(self):
        if self.move:
            self.y += self.speed
            self.x -= 2
            if self.y < 105:
                self.speed *= -1
            elif self.y > self.game.display.height - 105 - 40:
                self.speed *= -1


    def render(self):
        self.game.display.blit(self.image, (self.x, self.y))
        #pygame.draw.rect(self.game.display, (0,0,0), self.rect())


