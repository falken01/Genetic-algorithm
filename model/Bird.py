import math

import pygame
import os


class Bird:
    IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("sprites", "bird.png")))

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = 0
        self.velocity = 0

    def move(self):
        self.x += self.velocity
        self.y += 0.00006 * math.pow(self.y+58, 2)
        if self.y > 800:
            self.jump()

    def jump(self):
        self.y -= 35

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.IMG)
