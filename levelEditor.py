import pygame
import sys
from utils import *
from map import Map

MAP = 2

class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Edytor")
        self.screen = pygame.display.set_mode((1280, 768))
        self.display = pygame.Surface((640, 384))  # 20x12 tiles
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.assets = {
            'enemy': load_sheet('enemy1.png', 40, 40, 1, 8)[0],
            'field': load_image('field.png')
        }

        self.speed = 10

        self.pos = 0

        self.offset = 0

        self.movement = [0, 0]

        self.map = Map(self)

        try:
            self.map.load(f'map{MAP}.json')
        except FileNotFoundError:
            pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.movement[1] = True
                if event.key == pygame.K_a:
                    self.movement[0] = True
                if event.key == pygame.K_o:
                    self.map.save(f'map{MAP}.json')

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.movement[1] = False
                if event.key == pygame.K_a:
                    self.movement[0] = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    mouse = [mouse[0]//2, mouse[1]//2]
                    self.map.positions.append((mouse[0]+self.offset-20, mouse[1]-20))

                if event.button == 3:
                    mouse = pygame.mouse.get_pos()
                    mouse = [mouse[0] // 2, mouse[1] // 2]
                    for position in self.map.positions:
                        if pygame.rect.Rect(position, [40, 40]).collidepoint((mouse[0]+self.offset, mouse[1])):
                            self.map.positions.remove(position)



    def update(self):
        if not (self.offset == 0 and self.movement[1]-self.movement[0] < 0):
            self.offset += (self.movement[1]-self.movement[0])*self.speed

    def render_field(self):
        for i in range(20):
            self.display.blit(self.assets['field'], (i*144-self.offset, 0))

    def render(self):
        self.render_field()
        self.map.render(self.offset)
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        pygame.display.update()

    def run(self):
        while True:
            print(self.offset+self.display.width)
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

Editor().run()