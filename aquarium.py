import pygame as pg
import numpy as np
import time
from random import randint
import os

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TURQUOISE = (48, 213, 255)
BACKGROUND = TURQUOISE
Y_TOP_OFFSET = 150
Y_BOTTOM_OFFSET = 150
SCREEN_WIDTH = 1600
SCREEN_HIGHT = 1200
MIN_FISH_LENGHT = 50
MAX_FISH_LENGHT = 200
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HIGHT)

game_folder = os.path.dirname(__file__)
images_folder = os.path.join(game_folder, "img")


def current_milli_time():
    return round(time.time() * 1000)


class Fish(pg.sprite.Sprite):
    def __init__(self):
        self.direction = randint(0, 1)
        if self.direction == 0:
            # слева направо
            self.image = pg.image.load(os.path.join(images_folder, "fish7R.png"))
            self.length = self.image.get_width()
            self.xcoord = 0 - self.length
            self.speed = randint(1, 3)
        else:
            # справа налево
            self.image = pg.image.load(os.path.join(images_folder, "fish7L.png"))
            self.length = self.image.get_width()
            self.xcoord = SCREEN_WIDTH + self.length
            self.speed = randint(-3, -1)
        self.image.set_colorkey(WHITE)
        self.ycoord = randint(Y_TOP_OFFSET, SCREEN_HIGHT - Y_BOTTOM_OFFSET)
        self.rect = self.image.get_rect()
        self.rect.y = self.ycoord
        #  self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        #  self.color = (randint(60, 150), 125, 60)
        self.alive = True

    def update(self):
        self.xcoord += self.speed
        if self.xcoord < 0 - self.length or self.xcoord > SCREEN_WIDTH + self.length:
            self.alive = False
        self.rect.x = self.xcoord

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Worm():
    def __init__(self):
        self.direction = randint(0, 1)
        self.length = randint(MIN_FISH_LENGHT, MAX_FISH_LENGHT)
        if self.direction == 0:
            # слева направо
            self.xcoord = 0 - self.length
            self.speed = randint(1, 3)
        else:
            # справа налево
            self.xcoord = SCREEN_WIDTH + self.length
            self.speed = randint(-3, -1)
        self.ycoord = randint(Y_TOP_OFFSET, SCREEN_HIGHT - Y_BOTTOM_OFFSET)
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        #  self.color = (randint(60, 150), 125, 60)
        self.alive = True

    def update(self):
        self.xcoord += self.speed
        if self.xcoord < 0 - self.length or self.xcoord > SCREEN_WIDTH + self.length:
            self.alive = False

    def draw(self, screen):
        if self.alive:
            pg.draw.line(screen, self.color, (self.xcoord, self.ycoord), (self.xcoord + self.length, self.ycoord), 5)
            if self.direction == 0:
                pg.draw.circle(screen, self.color, (self.xcoord + self.length, self.ycoord), self.length * 0.05, 0)
            else:
                pg.draw.circle(screen, self.color, (self.xcoord, self.ycoord), self.length * 0.05, 0)


class GameManager:
    def __init__(self, screen):
        self.worms = []
        self.fishes = []
        self.screen = screen
        self.last_created_time_fish = current_milli_time()  # время создания последней рыбы в миллисекундах
        self.last_created_time_worm = current_milli_time()
        self.when_create_new_worm = 2000  # через сколько миллисекунд создать новую рыбу
        self.when_create_new_fish = 2000

    def try_to_create_fish(self):
        current_time = current_milli_time()
        delta = current_time - self.last_created_time_fish
        if delta >= self.when_create_new_fish:
            fish = Fish()
            self.fishes.append(fish)
            self.last_created_time_fish = current_milli_time()
            self.when_create_new_fish = randint(1000, 3000)

    def try_to_create_worm(self):
        current_time = current_milli_time()
        delta = current_time - self.last_created_time_worm
        if delta >= self.when_create_new_worm:
            worm = Worm()
            self.worms.append(worm)
            self.last_created_time_worm = current_milli_time()
            self.when_create_new_worm = randint(1000, 3000)

    def process(self, events, screen):
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
        return done

    def update(self):
        self.try_to_create_worm()
        for worm in self.worms:
            worm.update()
        self.try_to_create_fish()
        for fish in self.fishes:
            fish.update()

    def draw(self):
        for worm in self.worms:
            worm.draw(self.screen)
        for fish in self.fishes:
            fish.draw(self.screen)


def main():
    pg.init()
    pg.font.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption("Aquarium")
    done = False
    clock = pg.time.Clock()
    mgr = GameManager(screen)
    while not done:
        clock.tick(FPS)
        screen.fill(BACKGROUND)
        done = mgr.process(pg.event.get(), screen)
        mgr.update()
        mgr.draw()
        pg.display.flip()
    pg.quit


main()
