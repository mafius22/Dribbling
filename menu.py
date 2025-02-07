import pygame


class Menu:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.menu = True
        self.buttons = [pygame.rect.Rect(self.game.display.width // 2 - 100, self.game.display.height // 2 - 50, 200, 100)]

    def renderMenu(self, pos):
        for button in self.buttons:
            #self.game.display.blit(self.game.assets['startButton'], (button[0] - 70, button[1] - 40))
            if button.collidepoint(pos[0]//2, pos[1]//2):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                #self.game.display.blit(self.game.assets['startButton2'], (button[0] - 70, button[1] - 40))

    def klickButtons(self, pos):
        if self.buttons[0].collidepoint(pos[0]//2, pos[1]//2):
            pygame.mouse.set_visible(False)
            self.game.music['click'].play()
            self.start()

    def start(self):
        self.menu = False
