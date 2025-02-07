import pygame


class Player:
    def __init__(self, game):
        self.game = game
        self.y = self.game.display.height//2
        self.x = 100
        self.normalSpeed = 3
        self.speed = self.normalSpeed
        self.size = (40, 40)
        self.animation = self.game.assets['player/run'].copy()
        self.head_image = self.game.assets['player/head']
        self.ball_animation = self.game.assets['ball'].copy()

        self.kickedBall = False
        self.ballPos = [0, 0]

        self.time = 0

    def keep_in_field(self):
        if self.y < 0:
            self.reset()
            if self.game.goal:
                self.game.music['boo'].play()
        if self.y > self.game.display.height - self.size[1] - 5:
            self.reset()
            self.game.goalkeeper.reset()
            if self.game.goal:
                self.game.music['boo'].play()

    def rect(self):
        return pygame.rect.Rect(self.x+8, self.y+8, self.size[0]-16, self.size[1]-16)

    def update(self, movement, enemies):
        if movement:
            self.y -= self.speed
        else:
            self.y += self.speed

        for enemy in enemies:
            if enemy.rect().colliderect(self.rect()):
                self.kickedBall = True
                if self.ballPos == [0, 0]:
                    self.game.music['boo'].play()
                    self.ballPos = [self.x+30, self.y+20]

        if self.game.goalkeeper.rect().colliderect(self.rect()):
            self.kickedBall = True
            if self.ballPos == [0, 0]:
                self.game.music['boo'].play()
                self.ballPos = [self.x + 30, self.y + 20]

        if self.kickedBall:
            self.ballPos[0] -= 4
            self.time += 1
            if self.time == 50:
                self.reset()
                self.game.goalkeeper.reset()

        self.animation.update()
        self.ball_animation.update()
        self.keep_in_field()

    def reset(self):
        self.y = self.game.display.height // 2
        self.x = 100
        self.game.end_offset = 0
        self.game.loadEnemies()
        self.kickedBall = False
        self.ballPos = [0, 0]
        self.time = 0
        self.game.goal = True
        self.game.music['ankara_messi'].stop()

    def render(self, movement):
        if movement:
            self.game.display.blit(self.animation.img(), (self.x, self.y))
            if not self.kickedBall:
                self.game.display.blit(pygame.transform.flip(self.ball_animation.img(), False, True), (self.x+25, self.y+5))
            self.game.display.blit(self.head_image, (self.x, self.y))
        else:
            self.game.display.blit(pygame.transform.flip(self.animation.img(), False, True), (self.x, self.y))
            if not self.kickedBall:
                self.game.display.blit(self.ball_animation.img(), (self.x+20, self.y+25))
            self.game.display.blit(pygame.transform.flip(self.head_image, False, True), (self.x, self.y))
        #pygame.draw.rect(self.game.display, (0,0,0), self.rect())
        if self.kickedBall:
            self.game.display.blit(pygame.transform.flip(self.ball_animation.img(), False, True), self.ballPos)


