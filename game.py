import pygame
import sys
from player import Player
from enemy import Enemy
from map import Map
from utils import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
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

        self.music = {
            'goal': pygame.mixer.Sound("data/music/free-crowd-cheering-sounds-02-strong-cheering-rhythmic-cheering-116190 (mp3cut.net).mp3"),
            'messi': pygame.mixer.Sound("data/music/Voicy_Messi, Messi, Messi.mp3"),
            'boo': pygame.mixer.Sound("data/music/crowd-large-outrage-then-booing-reaction-hockey-game-2011-25915 (mp3cut.net).mp3"),
        }

        self.songs = ["data/music/IShowSpeed - World Cup (Official Music Video) (mp3cut.net).mp3", "data/music/We Are One (Ole Ola) [The Official 2014 FIFA World Cup Song] (Olodum Mix).mp3"]

        self.moving = False
        self.moving_mode = False
        self.offset = 0
        self.end_offset = 0
        self.paused = False
        self.goal = True

        self.player = Player(self)

        self.map = Map(self)

        self.level = 0

        self.loadEnemies()

    def start_music(self):
        pygame.mixer.music.load(self.songs[0])
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()
        for song in self.songs[1:]:
            pygame.mixer.music.queue(song)

    def loadEnemies(self):
        try:
            self.map.load(f'map{self.level}.json')
        except FileNotFoundError:
            pass

        self.enemies = []
        for position in self.map.positions:
            self.enemies.append(Enemy(self, *position))

    def update(self):
        if not self.paused:
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if not self.paused:
                        self.moving = False
                        self.player.speed = 0
                        for enemy in self.enemies:
                            enemy.speed = 0
                        self.paused = not self.paused
                    else:
                        self.player.speed = self.player.normalSpeed
                        for enemy in self.enemies:
                            enemy.speed = enemy.normalSpeed
                        self.paused = not self.paused

            if self.moving_mode:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.moving = not self.moving
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.paused:

                        self.moving = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and not self.paused:
                        self.moving = False

    def render_field(self):
        print(self.level)
        self.offset %= 144
        for i in range(6 - self.end_offset//144):
            self.display.blit(self.assets['field'], (i*144-self.offset, 0))
        if len(self.enemies) == 0:
            self.display.blit(self.assets['field2'], (self.display.width-self.end_offset + 72, 0))
            self.display.blit(self.assets['trybuny'], (self.display.width - self.end_offset + 72 + 144, 0))
            if self.goal:
                self.goal = False
                self.music['goal'].play()
            if not self.paused:
                self.end_offset += 2
                self.offset += 1
            if self.display.width-self.end_offset + 72 + 100 == self.player.x and self.player.y > 101 and self.player.y + 40 < self.display.height - 105:
                self.level += 1
                self.player.reset()
                self.end_offset = 0
            elif self.display.width-self.end_offset + 72 + 100 == self.player.x and not (self.player.y > 101 and self.player.y + 40 < self.display.height - 105):
                self.player.reset()

        if not self.paused:
            self.offset += 1


    def render(self):
        self.render_field()
        for enemy in self.enemies:
            enemy.render()
        self.player.render(self.moving)
        if len(self.enemies) == 0:
            self.display.blit(self.assets['field3'], (self.display.width - self.end_offset + 72 + 144 - 27, 101))

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        if self.paused:
            self.screen.fill((50,50,50), special_flags=pygame.BLEND_RGBA_MULT)
        pygame.display.update()

    def run(self):
        self.start_music()
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

Game().run()