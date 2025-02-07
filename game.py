import pygame
import sys
from player import Player
from enemy import Enemy
from map import Map
from utils import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Dribbling")
        self.screen = pygame.display.set_mode((1280, 768))
        self.display = pygame.Surface((640, 384))  # 20x12 tiles
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.assets = {
            'player/run': Animation(load_sheet('player.png', 40, 40, 1, 8), loop=True, img_dur=5),
            'player/head': load_image('player_head.png'),
            'enemy1/run': Animation(load_sheet('enemy1.png', 40, 40, 1, 8), loop=True, img_dur=5),
            'enemy2/run': Animation(load_sheet('enemy2.png', 40, 40, 1, 8), loop=True, img_dur=5),
            'ball': Animation(load_sheet('ball.png', 16, 16, 1, 4), loop=True, img_dur=5),
            'field': load_image('field.png'),
            'field2': pygame.image.load('data/images/field2.png').convert_alpha(),
            'field3': load_image('field3.png'),
            'trybuny': pygame.image.load('data/images/trybuny.png').convert_alpha(),
        }

        self.moving = False
        self.moving_mode = False
        self.offset = 0
        self.end_offset = 0

        self.player = Player(self)

        self.map = Map(self)

        self.level = 0

        try:
            self.map.load(f'map{self.level}.json')
        except FileNotFoundError:
            pass

        self.loadEnemies()


    def loadEnemies(self):
        self.enemies = []
        for position in self.map.positions:
            self.enemies.append(Enemy(self, *position))

    def update(self):
        for enemy in self.enemies:
            enemy.update()
            if enemy.remove:
                self.enemies.remove(enemy)
        self.player.update(self.moving, self.enemies)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.moving_mode:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.moving = not self.moving
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.moving = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.moving = False

    def render_field(self):
        self.offset %= 144
        for i in range(6 - self.end_offset//144):
            self.display.blit(self.assets['field'], (i*144-self.offset, 0))
        if len(self.enemies) == 0:
            self.display.blit(self.assets['field2'], (self.display.width-self.end_offset + 72, 0))
            self.display.blit(self.assets['trybuny'], (self.display.width - self.end_offset + 72 + 144, 0))
            self.end_offset += 2
            self.offset += 1
            if self.display.width-self.end_offset + 72 + 100 == self.player.x and self.player.y > 101 and self.player.y + 40 < self.display.width - 101:
                self.player.reset()
                self.end_offset = 0
        self.offset += 1

    def render(self):
        self.render_field()
        for enemy in self.enemies:
            enemy.render()
        self.player.render(self.moving)
        if len(self.enemies) == 0:
            self.display.blit(self.assets['field3'], (self.display.width - self.end_offset + 72 + 144 - 27, 101))
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        pygame.display.update()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

Game().run()