import pygame
import sys
from player import Player
from enemy import Enemy
from map import Map
from goalkeeper import Goalkeeper
from utils import *
from menu import Menu
import random
import math

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Dribbling")
        self.screen = pygame.display.set_mode((1280, 768))
        self.display = pygame.Surface((640, 384))  # 20x12 tiles
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.max_level = 5
        self.assets = {
            'player/run': Animation(load_sheet('player.png', 40, 40, 1, 8), loop=True, img_dur=5),
            'player/head': load_image('player_head.png'),
            'enemy0/run': Animation(load_sheet('enemy1.png', 40, 40, 1, 8), loop=True, img_dur=5),
            'enemy1/run': Animation(load_sheet('enemy2.png', 40, 40, 1, 8), loop=True, img_dur=5),
            'ball': Animation(load_sheet('ball.png', 16, 16, 1, 4), loop=True, img_dur=5),
            'field': load_image('field.png'),
            'win': pygame.image.load('data/images/leomess.png').convert_alpha(),
            'field2': pygame.image.load('data/images/field2.png').convert_alpha(),
            'field3': load_image('field3.png'),
            'trybuny': pygame.image.load('data/images/trybuny.png').convert_alpha(),
            'goalkeeper': load_image('goalkeeper.png'),
            'startButton': load_image('barcelona2.png'),
            'startButton2': load_image('barcelona2.3.png'),
            'leo': load_image('leosipiwo2.jpg'),
            'trophy': load_image('trophy.png'),
            'ronaldo': load_image('ronaldo.png'),
            'wojciech': load_image('wojciech.png'),
            'slawek': load_image('slawek.png'),
        }

        self.music = {
            'goal': pygame.mixer.Sound("data/music/goal_sound.mp3"),
            'before_goal': pygame.mixer.Sound("data/music/before_goal_sound.mp3"),
            'messi': pygame.mixer.Sound("data/music/Voicy_Messi, Messi, Messi.mp3"),
            'ankara_messi': pygame.mixer.Sound("data/music/gol-messi-vs-getafe-narrat-per-puyal-full-hd-1080p-audiotrimmer.mp3"),
            'boo': pygame.mixer.Sound("data/music/crowd-large-outrage-then-booing-reaction-hockey-game-2011-25915 (mp3cut.net).mp3"),
        }

        self.songs = ["data/music/We Are One (Ole Ola) [The Official 2014 FIFA World Cup Song] (Olodum Mix).mp3", "data/music/IShowSpeed - World Cup (Official Music Video) (mp3cut.net).mp3",
                       'data/music/Olele, Olala.mp3']

        self.moving = False
        self.moving_mode = False
        self.offset = 0
        self.end_offset = 0
        self.paused = False
        self.goal = True

        self.time = 0
        self.timeMessi = 0

        self.player = Player(self)

        self.goalkeeper = Goalkeeper(self)

        self.map = Map(self)

        self.menu = Menu(self)

        self.level = 0

        self.win = False
        self.win_music_played = False

        self.count = 0 

        self.loadEnemies()


    def start_music(self):
        pygame.mixer.music.load(self.songs[0])
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()
        for song in self.songs[1:]:
            pygame.mixer.music.queue(song)

    def loadEnemies(self):
        self.time = 0
        self.timeMessi = 0
        try:
            self.map.load(f'data/maps/map{self.level}.json')
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
            self.goalkeeper.update()
            self.player.update(self.moving, self.enemies)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not self.menu.menu:
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
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.menu.klickButtons(pygame.mouse.get_pos())


    def render_field(self):
        self.offset %= 144
        for i in range(6 - self.end_offset//144):
            self.display.blit(self.assets['field'], (i*144-self.offset, 0))
        if len(self.enemies) == 0:
            self.display.blit(self.assets['field2'], (self.display.width-self.end_offset + 72, 0))
            self.display.blit(self.assets['trybuny'], (self.display.width - self.end_offset + 72 + 144, 0))
            if self.time == 100:
                self.music['before_goal'].play()
            self.time += 1
            if self.goal:
                self.goalkeeper.move = True
                self.goal = False
            if not self.paused:
                self.end_offset += 2
                self.offset += 1
            if self.display.width-self.end_offset + 72 + 100 == self.player.x and self.player.y > 101 and self.player.y + 40 < self.display.height - 105 and  not self.player.kickedBall:
                self.music['goal'].play()
                self.level += 1
                self.player.reset()
                self.goalkeeper.reset()
                self.end_offset = 0
            elif self.display.width-self.end_offset + 72 + 100 == self.player.x and not (self.player.y > 101 and self.player.y + 40 < self.display.height - 105):
                self.player.reset()
                self.goalkeeper.reset()

        if not self.paused:
            self.offset += 1


    def render(self):
        self.render_field()
        for enemy in self.enemies:
            enemy.render()
        self.goalkeeper.render()
        self.player.render(self.moving)
        if len(self.enemies) == 0:
            self.display.blit(self.assets['field3'], (self.display.width - self.end_offset + 72 + 144 - 27, 101))
        pygame.display.update()

    def music_effects(self):
        if self.level == 2:
            if self.timeMessi == 750:
                self.music['messi'].play()
            self.timeMessi += 1

        if self.level == 5:
            if self.timeMessi == 590:
                self.music['ankara_messi'].play()
            self.timeMessi += 1

    def check_win(self):
        if self.level > self.max_level:
            self.win = True
    
    def run(self):
        self.start_music()
        while True:
            if not self.menu.menu:
                if not self.win:
                    self.update()
                    self.render()
                    self.music_effects()
                    self.check_win()
                else:
                    self.run_win_screen()
            else:
                self.menu.renderMenu(pygame.mouse.get_pos())
            self.handle_events()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            if self.paused:
                self.screen.fill((50, 50, 50), special_flags=pygame.BLEND_RGBA_MULT)
            pygame.display.update()
            self.clock.tick(self.fps)

    def run_win_screen(self):
            if self.count < 250:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()

                self.display.fill((0,0,0))
                self.count += 1

            else:
                offset_y = math.sin(pygame.time.get_ticks() * 0.006) * 15

                center_x = self.display.get_width() // 2
                center_y = self.display.get_height() // 2

                win_image = self.assets['win']
                win_rect = win_image.get_rect(center=(center_x, center_y + offset_y))

                self.display.blit(win_image, win_rect)

                if not self.win_music_played:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(self.songs[2])
                    pygame.mixer.music.play(0)
                    self.win_music_played = True

Game().run()