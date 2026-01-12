import pygame


class Menu:
    def __init__(self, game):
        self.game = game
        self.button = pygame.rect.Rect(self.game.display.width//2-50, self.game.display.height//2-50, 100, 100)
        self.menu = True

    def renderMenu(self, pos):
        self.game.display.blit(self.game.assets['leo'], (-320,-120))
        self.game.display.blit(self.game.assets['startButton'], self.button)
        self.game.display.blit(self.game.assets['trophy'], (115,100))
        if self.button.collidepoint(pos[0]//2, pos[1]//2):
            self.game.display.blit(self.game.assets['startButton2'], self.button)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


        if pygame.rect.Rect(118, 100, 35, 100).collidepoint(pos[0]//2, pos[1]//2):
            self.game.display.blit(self.game.assets['ronaldo'], (self.game.display.width-100, self.game.display.height-100))


        #pygame.draw.rect(self.game.display, (0, 0, 0), rect)
        if pygame.rect.Rect(560, 150, 30, 30).collidepoint(pos[0]//2, pos[1]//2):
            self.game.display.blit(self.game.assets['wojciech'], (0, self.game.display.height-187))


        if pygame.rect.Rect(527, 110, 33, 90).collidepoint(pos[0] // 2, pos[1] // 2):
            self.game.display.blit(self.game.assets['slawek'], (self.game.display.width-123, 0))



    def klickButtons(self, pos):
        if self.button.collidepoint(pos[0]//2, pos[1]//2):
            self.menu = False
