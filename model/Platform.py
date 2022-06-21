import pygame
import os


class Platform:
    PLATFORM_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("sprites", "base.png")))

    def __init__(self):
        self.x1 = 0
        self.x2 = 672
        self.y = 750
        self.vel = 5

    def draw(self, win):
        self.move()
        win.blit(self.PLATFORM_IMG, (self.x1, self.y))
        win.blit(self.PLATFORM_IMG, (self.x2, self.y))

    def move(self):
        self.x1 -= 5
        self.x2 -= 5
        if self.x1 < -670:
            self.x1 = 668
        elif self.x2 < -670:
            self.x2 = 668
