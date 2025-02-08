import pygame


class Menu:
    def __init__(self, game):
        self.game = game
        self.button = pygame.rect.Rect(self.game.display.width//2-50, self.game.display.height//2-50, 100, 100)
        self.menu = True

    def renderMenu(self, pos):
        self.game.display.blit(self.game.assets['leo'], (-300,-120))
        self.game.display.blit(self.game.assets['startButton'], self.button)
        if self.button.collidepoint(pos[0]//2, pos[1]//2):
            self.game.display.blit(self.game.assets['startButton2'], self.button)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def klickButtons(self, pos):
        if self.button.collidepoint(pos[0]//2, pos[1]//2):
            self.menu = False
