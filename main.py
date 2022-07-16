import pygame
import os
import random

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
        self.start_x = 330
        self.start_y = 350

        # Optimization variables init
        self.optimization = False
        self.population_number = 5
        self.iteration_number = 2
        self.mutation_probability = 0.05
        self.cross_probability = 0.8
        self.tournament_population = self.population_number  # the same as population_number
        self.tournament_k_value = 3

    def draw(self, bird, platform, pipes):
        self.win.blit(self.BG_IMG, (0, 0))
        for pipe in pipes:
            pipe.draw(self.win)
        platform.draw(self.win)
        bird.draw(self.win)
        pygame.display.update()

    def main(self):
        # Setting up a game parameters
        pipes = [Pipe.Pipe(500), Pipe.Pipe(900)]
        platform = Platform.Platform()
        bird = Bird.Bird(self.start_x, self.start_y)

        # normal game play
        if not self.optimization:
            bird2 = Bird.Bird(330, 0)
            bird3 = Bird.Bird(330, 700)
            bird4 = Bird.Bird(330, 350)

            # Launching the game
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
                # self.draw(bird2,platform, pipes)
                # self.draw(bird3,platform, pipes)
                # self.draw(bird4,platform, pipes)

            pygame.quit()
            quit()


        # Optimization automatic gameplay
        else:
            # generating basic population
            population_jump = []
            number_of_jumps = 150
            for i in range(self.population_number):
                tmp = []
                for j in range(number_of_jumps):
                    # getting random place of jump
                    if j == 0:
                        tmp.append(random.randint(self.start_y, 700))
                    tmp.append(random.randint(tmp[j] - 35, 700))
                population_jump.append(tmp)

            # puszczenie calej populacji w grze - zwrot wynikow (results) jako pkt oceny - im
            # wiecej pkt tym lepsza ocena.

            scores = []

            # Launching the game
            for i in range(self.population_number):
                k = 0
                del bird
                bird = Bird.Bird(330, 350)
                # wyczy plansze!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                while self.runGame and k < 150:
                    if bird.y >= population_jump[i][k]:
                        bird.jump()
                        k += 1
                    bird.move()

                    for pipe in pipes:
                        if bird.x > pipe.x and not pipe.passed:
                            bird.points += 1
                            pipe.passed = True

                        if pipe.collide(bird, pipe):
                            self.runGame = False
                scores.append(bird.points)

            tmp = max(scores)
            best_of = [population_jump[scores.index(tmp)], tmp]

            # Main iteration loop
            for i in range(self.iteration_number):

                # Creating tournament list
                tournament_list = []
                for l in range(self.population_number):
                    for m in range(scores[l] + 1): tournament_list.append([population_jump[l], scores[l]])
                # Tournament selection
                winners = []
                for j in range(self.tournament_population):
                    tmpi = random.choices(tournament_list, k=self.tournament_k_value)
                    winners.append(sorted(tmpi, key=lambda x: x[1], reverse=True)[0][0])

                # Genetic - mutation and crossing.
                for l in range(self.population_number):
                    for m in range(number_of_jumps):
                        if random.random() < self.mutation_probability:
                            if m == 0:
                                winners[l][m] = random.randint(self.start_y, 700)
                            else:
                                winners[l][m] = random.randint(winners[l][m - 1] - 35, 700)
                        elif random.random() < self.cross_probability:
                            winners[l][m] += int(random.random() * (winners[l][m] - best_of[0][m]))

                        if winners[l][m] >= 700: winners[l][m] = 699

                # Genetic population scoring - Launching the game
                genetic_scores = []
                for j in range(self.population_number):
                    k = 0
                    del bird
                    bird = Bird.Bird(330, 350)
                    # wyczyscic plansze!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    while self.runGame and k < 150:
                        if bird.y >= population_jump[j][k]:
                            bird.jump()
                            k += 1
                        bird.move()

                        for pipe in pipes:
                            if bird.x > pipe.x and not pipe.passed:
                                bird.points += 1
                                pipe.passed = True

                            if pipe.collide(bird, pipe):
                                self.runGame = False
                    genetic_scores.append(bird.points)

                # Succesion
                genetic_list = []
                for l in range(self.tournament_population):
                    for m in range(genetic_scores[l] + 1): genetic_list.append([winners[l], genetic_scores[l]])
                tmp = sorted(tournament_list + genetic_list, key=lambda x: x[1], reverse=True)[:self.population_number]
                population_jump = []
                for x in tmp:
                    population_jump.append(x[0])
                print(population_jump)

                if tmp[0][1] > best_of[1]:
                    best_of = tmp[0]


# trzeba przywracac plansze do poczatku! - dopisac to w ocenie populacji genetycznej


game = Game()
game.main()
