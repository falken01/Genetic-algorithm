import pygame
import os
from model import Bird
from model import Pipe
from model import Platform


class Game:
    BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("sprites", "bg.png")))

    def __init__(self):
        self.points = 0
        self.runGame = True
        self.SCREEN_HEIGHT = 800
        self.SCREEN_WIDTH = 576
        self.win = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.CLOCK = pygame.time.Clock()

    def draw(self, bird, platform, pipes):
        self.win.blit(self.BG_IMG, (0, 0))
        for pipe in pipes:
            pipe.draw(self.win)
        platform.draw(self.win)
        bird.draw(self.win)
        pygame.display.update()

    def main(self):
        pipes = [Pipe.Pipe(500), Pipe.Pipe(900)]
        platform = Platform.Platform()
        bird = Bird.Bird(330, 350)
        while self.runGame:
            self.CLOCK.tick(25)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runGame = False

            userInput = pygame.key.get_pressed()
            if userInput[pygame.K_SPACE]:
                bird.jump()
            bird.move()

            for pipe in pipes:
                if bird.x > pipe.x and not pipe.passed:
                    bird.points += 1
                    pipe.passed = True

                if pipe.collide(bird, pipe):
                    self.runGame = False

            self.draw(bird, platform, pipes)

        pygame.quit()
        quit()


game = Game()
game.main()
