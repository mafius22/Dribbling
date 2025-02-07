import pygame
import json


class Map:
    def __init__(self, game):
        self.game = game
        self.positions = []

    def render(self, offset=0):
        for position in self.positions:
            self.game.display.blit(self.game.assets[f'enemy{position[2]}'], (position[0]-offset, position[1]))


    #def physics_rects_around(self, pos, k, l):
    #    rects = []
    #    pos = (int(pos[0]) // self.tile_size, int(pos[1]) // self.tile_size)
    #    for i in range(k, l):
    #        for j in range(k, l):
    #            key = f"{pos[0] + i};{pos[1] + j}"
    #            if key in self.tilemap:
    #                if self.tilemap[key] not in {28, 29, 30, 31, 32}:
    #                    rects.append(pygame.Rect(
    #                        (pos[0] + i) * self.tile_size,
    #                        (pos[1] + j) * self.tile_size,
    #                        self.tile_size,
    #                        self.tile_size
    #                    ))
    #                else:
    #                    rects.append(pygame.Rect(
    #                        (pos[0] + i) * self.tile_size,
    #                        (pos[1] + j) * self.tile_size,
    #                        self.tile_size,
    #                        self.tile_size-22
    #                    ))
    #    return rects



    def save(self, path):
        f = open(path, 'w')
        json.dump({'positions': self.positions}, f)
        f.close()

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        self.positions = map_data['positions']


