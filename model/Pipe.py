import pygame
import random
import os


class Pipe:
    IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("sprites", "pipe.png")))

    def __init__(self, x):
        self.border = None
        self.x = x
        self.pipeBottom = self.IMG
        self.pipeTop = pygame.transform.flip(self.IMG, False, True)
        self.y = self.setHeight()
        self.velocity = 5
        self.GAP = 850
        self.top = 0
        self.mid = x
        self.passed = False
        self.bottom = 0

    def setHeight(self):
        self.top = self.pipeTop.get_height()
        self.bottom = self.pipeBottom.get_height()
        rInt = random.randint(-500, -300)
        return rInt

    def move(self):
        for i in range(0, 2):
            self.x -= self.velocity
            if self.x < -100:
                self.x = 700
                self.y = self.setHeight()
                self.passed = False

    def draw(self, win):
        self.move()
        win.blit(self.pipeTop, (self.x, self.y))
        win.blit(self.pipeBottom, (self.x, self.y + self.GAP))

    def collide(self, bird, pipes):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipeTop)
        bottom_mask = pygame.mask.from_surface(self.pipeBottom)

        top_offset = (self.x - bird.x, self.y - round(bird.y))
        bottom_offset = (self.x - bird.x, self.y + self.GAP - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            print(self.pipeTop.get_height())
            return True
        return False
        # if bird_mask.overlap(bottom_mask, bottom_offset):
        #     print(self.pipeTop.get_rect().top)
