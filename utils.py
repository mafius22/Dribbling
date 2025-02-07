import pygame
import os

PATH = 'data/images/'

def load_image(data):
    image = pygame.image.load(PATH+data).convert_alpha()
    image.set_colorkey((255, 255, 255))
    return image


def load_sheet(data, frame_width, frame_height, rows, cols):
    images = []
    image = pygame.image.load(PATH+data).convert_alpha()
    image.set_colorkey((255, 255, 255))
    for row in range(rows):
        for col in range(cols):
            x = col * frame_width
            y = row * frame_height
            frame = image.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            images.append(frame)
    return images


def load_images(path):
    images = []
    for img_name in os.listdir(PATH + path):
        images.append(load_image(path + '/' + img_name))
    return images


def scale_images(images, scale):
    scaled_images = []
    for image in images:
        scaled_images.append(pygame.transform.scale(image, scale))

    return scaled_images

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def img(self):
        return self.images[int(self.frame / self.img_duration)]

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

