import pygame as pg
import numpy as np
import time
import math
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
COLLISION_DIST = 80
HOOK_UP = 1
HOOK_DOWN = 2
HOOK_LEFT = 3
HOOK_RIGHT = 4
HOOK_NONE = 0 
HOOK_STEP = 4


game_folder = os.path.dirname(__file__)
images_folder = os.path.join(game_folder, "img")


def calcDist(x1, y1, x2, y2):
    dist = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return dist


def current_milli_time():
    return round(time.time() * 1000)


class Fish(pg.sprite.Sprite):
    def __init__(self):
        self.hasCollisions = False
        self.direction = randint(0, 1)
        if self.direction == 0:
            # слева направо
            a = randint(1, 3)
            if a == 1:
                self.image = pg.image.load(os.path.join(images_folder, "fish7R.png"))
            if a == 2:
                self.image = pg.image.load(os.path.join(images_folder, "fish8R.png"))
            if a == 3:
                self.image = pg.image.load(os.path.join(images_folder, "fish9R.png"))

            self.length = self.image.get_width()
            self.height = self.image.get_height()
            self.xcoord = 0 - self.length
            self.speed = randint(1, 3)
        else:
            # справа налево
            b = randint(1, 3)
            if b == 1:
                self.image = pg.image.load(os.path.join(images_folder, "fish7L.png"))
            if b == 2:
                self.image = pg.image.load(os.path.join(images_folder, "fish8L.png"))
            if b == 3:
                self.image = pg.image.load(os.path.join(images_folder, "fish9L.png"))
            self.length = self.image.get_width()
            self.height = self.image.get_height()
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

    def calcMouthCoord(self):
        if self.direction == 0:
            #  направо
            x = self.xcoord + self.length
            y = self.ycoord + self.height / 2
        else:
            # налево
            x = self.xcoord
            y = self.ycoord + self.height / 2
        return x, y

    def calcTailCoord(self):
        if self.direction == 0:
            #  направо
            x = self.xcoord
            y = self.ycoord + self.height / 2
        else:
            # налево
            x = self.xcoord + self.length
            y = self.ycoord + self.height / 2
        return x, y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Hook():
    def __init__(self):
        self.image = pg.image.load(os.path.join(images_folder, "hook.png"))
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = (SCREEN_WIDTH - self.rect.width) / 2
        self.image.set_colorkey(WHITE)
        self.stateV = HOOK_UP
        self.stateH = HOOK_NONE

    def draw(self,screen):
            screen.blit(self.image, self.rect)

    def update(self):
        if self.stateV == HOOK_UP:
            if self.rect.y > 0:
                self.rect.y -= HOOK_STEP
            if self.rect.y < 0:
                self.rect.y = 0
        else:
            #  HOOK_DOWN
            yMax = SCREEN_HIGHT - self.rect.width - 20
            if self.rect.y < yMax:
                self.rect.y += HOOK_STEP
            if self.rect.y > yMax:
                self.rect.y = yMax
        if self.stateH == HOOK_RIGHT:
            xMax = SCREEN_WIDTH - self.rect.width - 5
            if self.rect.x < xMax:
                self.rect.x += HOOK_STEP
            if self.rect.x > xMax:
                self.rect.x = xMax
        elif self.stateH == HOOK_LEFT:
            xMin = 0 + 5
            if self.rect.x > xMin:
                self.rect.x -= HOOK_STEP
            if self.rect.x < xMin:
                self.rect.x = xMin






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
        self.hook = Hook()
        self.screen = screen
        self.last_created_time_fish = current_milli_time()  # время создания последней рыбы в миллисекундах
        self.last_created_time_worm = current_milli_time()
        self.when_create_new_worm = 2000  # через сколько миллисекунд создать новую рыбу
        self.when_create_new_fish = 2000

    def try_to_create_fish(self, fish=Fish):
        current_time = current_milli_time()
        delta = current_time - self.last_created_time_fish
        if delta >= self.when_create_new_fish:
            cnt = len(self.fishes)
            found = -1
            for index in range(0, cnt):
                fish = self.fishes[index]
                if fish.alive == False:
                    found = index
                    break
            if found == -1:
                fish = Fish()
                self.fishes.append(fish)
            else:
                self.fishes[found] = Fish()
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
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    self.hook.stateV = HOOK_DOWN
                elif event.key == pg.K_LEFT:
                    self.hook.stateH = HOOK_LEFT
                elif event.key == pg.K_RIGHT:
                    self.hook.stateH = HOOK_RIGHT
            elif event.type == pg.KEYUP:
                if event.key == pg.K_DOWN:
                    self.hook.stateV = HOOK_UP
                elif event.key == pg.K_LEFT:
                    self.hook.stateH = HOOK_NONE
                elif event.key == pg.K_RIGHT:
                    self.hook.stateH = HOOK_NONE

        return done

    def update(self):
        #         self.try_to_create_worm()
        #         for worm in self.worms:
        #             worm.update()
        self.try_to_create_fish()
        for fish in self.fishes:
            fish.update()
        self.hook.update()

    def draw(self):
        for worm in self.worms:
            worm.draw(self.screen)
        for fish in self.fishes:
            fish.draw(self.screen)
        self.hook.draw(self.screen)

    # на основе расстояния, определяемого по теореме пифагора
    # def collision(self, fish1: Fish, fish2: Fish):
    #     changed = False
    #     if fish1.direction != fish2.direction:
    #         x1, y1 = fish1.calcMouthCoord()
    #         x2, y2 = fish2.calcMouthCoord()
    #         dist = calcDist(x1, y1, x2, y2)
    #         if dist <= COLLISION_DIST:
    #             #  print(f"[1]x1={x1},y1={y1},x2={x2},y2={y2},dist={dist},dir={fish1.direction}")
    #             fish1.direction = 1 - fish1.direction
    #             fish1.speed = -fish1.speed
    #             fish1.image = pg.transform.flip(fish1.image, True, False)
    #             fish2.direction = 1 - fish2.direction
    #             fish2.speed = -fish2.speed
    #             fish2.image = pg.transform.flip(fish2.image, True, False)
    #             #  print(f"[2]x1={x1},y1={y1},x2={x2},y2={y2},dist={dist},dir={fish1.direction}")
    #             changed = True
    #             fish1.hasCollisions = True
    #     else:
    #         if fish1.direction == 0:
    #             #  обе вправо
    #             if fish2.rect.x >= fish1.rect.x:
    #                 #  fish1 догоняет рыбу fish2
    #                 x1, y1 = fish1.calcMouthCoord()
    #                 x2, y2 = fish2.calcTailCoord()
    #                 dist = calcDist(x1, y1, x2, y2)
    #                 if dist <= COLLISION_DIST:
    #                     fish1.direction = 1 - fish1.direction
    #                     fish1.speed = -fish1.speed
    #                     fish1.image = pg.transform.flip(fish1.image, True, False)
    #             else:
    #                 #   рыбу fish1 догоняет fish2
    #                 x1, y1 = fish1.calcTailCoord()
    #                 x2, y2 = fish2.calcMouthCoord()
    #                 dist = calcDist(x1, y1, x2, y2)
    #                 if dist <= COLLISION_DIST:
    #                     fish2.direction = 1 - fish2.direction
    #                     fish2.speed = -fish2.speed
    #                     fish2.image = pg.transform.flip(fish2.image, True, False)
    #         else:
    #             # обе влево
    #             if fish2.rect.x <= fish1.rect.x:
    #                 #  fish1 догоняет рыбу fish2
    #                 x1, y1 = fish1.calcMouthCoord()
    #                 x2, y2 = fish2.calcTailCoord()
    #                 dist = calcDist(x1, y1, x2, y2)
    #                 if dist <= COLLISION_DIST:
    #                     fish1.direction = 1 - fish1.direction
    #                     fish1.speed = -fish1.speed
    #                     fish1.image = pg.transform.flip(fish1.image, True, False)
    #             else:
    #                 #   рыбу fish1 догоняет fish2
    #                 x1, y1 = fish1.calcTailCoord()
    #                 x2, y2 = fish2.calcMouthCoord()
    #                 dist = calcDist(x1, y1, x2, y2)
    #                 if dist <= COLLISION_DIST:
    #                     fish2.direction = 1 - fish2.direction
    #                     fish2.speed = -fish2.speed
    #                     fish2.image = pg.transform.flip(fish2.image, True, False)
    #     #  return fish1, fish2, changed

    def collision(self, fish1: Fish, fish2: Fish):
        minY = (fish1.rect.height / 2) + (fish2.rect.height / 2)
        #  minY =
        minX = 5
        changed = False
        if fish1.direction != fish2.direction:
            # навтречу друг другу
            x1, y1 = fish1.calcMouthCoord()
            x2, y2 = fish2.calcMouthCoord()
            deltaY = abs(y1 - y2)
            deltaX = abs(x1 - x2)
            if deltaY <= minY and deltaX <= minX:
                fish1.direction = 1 - fish1.direction
                fish1.speed = -fish1.speed
                fish1.speed += 1 if fish1.speed >= 0 else -1
                fish1.image = pg.transform.flip(fish1.image, True, False)
                fish2.direction = 1 - fish2.direction
                fish2.speed = -fish2.speed
                fish2.speed += 1 if fish2.speed >= 0 else -1
                fish2.image = pg.transform.flip(fish2.image, True, False)
                changed = True
                fish1.hasCollisions = True
        else:
            if fish1.direction == 0:
                #  обе вправо
                if fish2.rect.x >= fish1.rect.x:
                    x1, y1 = fish1.calcMouthCoord()
                    x2, y2 = fish2.calcTailCoord()
                    deltaY = abs(y1 - y2)
                    deltaX = abs(x1 - x2)
                    if deltaY <= minY and deltaX <= minX:
                        fish1.direction = 1 - fish1.direction
                        fish1.speed = -fish1.speed
                        fish1.speed += 1 if fish1.speed >= 0 else -1
                        fish1.image = pg.transform.flip(fish1.image, True, False)
                        changed = True
                else:
                    #   рыбу fish1 догоняет fish2
                    x1, y1 = fish1.calcTailCoord()
                    x2, y2 = fish2.calcMouthCoord()
                    deltaY = abs(y1 - y2)
                    deltaX = abs(x1 - x2)
                    if deltaY <= minY and deltaX <= minX:
                        fish2.direction = 1 - fish2.direction
                        fish2.speed = -fish2.speed
                        fish2.speed += 1 if fish2.speed >= 0 else -1
                        fish2.image = pg.transform.flip(fish2.image, True, False)
                        changed = True
            else:
                # обе влево
                if fish2.rect.x <= fish1.rect.x:
                    #  fish1 догоняет рыбу fish2
                    x1, y1 = fish1.calcMouthCoord()
                    x2, y2 = fish2.calcTailCoord()
                    deltaY = abs(y1 - y2)
                    deltaX = abs(x1 - x2)
                    if deltaY <= minY and deltaX <= minX:
                        fish1.direction = 1 - fish1.direction
                        fish1.speed = -fish1.speed
                        fish1.speed += 1 if fish1.speed >= 0 else -1
                        fish1.image = pg.transform.flip(fish1.image, True, False)
                        changed = True
                else:
                    #   рыбу fish1 догоняет fish2
                    x1, y1 = fish1.calcTailCoord()
                    x2, y2 = fish2.calcMouthCoord()
                    deltaY = abs(y1 - y2)
                    deltaX = abs(x1 - x2)
                    if deltaY <= minY and deltaX <= minX:
                        fish2.direction = 1 - fish2.direction
                        fish2.speed = -fish2.speed
                        fish2.speed += 1 if fish2.speed >= 0 else -1
                        fish2.image = pg.transform.flip(fish2.image, True, False)
                        changed = True
        return changed

    def collisions(self):
        cnt = len(self.fishes)
        #  print(f"cnt={cnt}")
        for index1 in range(0, cnt - 1):
            fish1 = self.fishes[index1]
            for index2 in range(index1 + 1, cnt):
                fish2 = self.fishes[index2]
                if fish1.alive and fish2.alive:
                    self.collision(fish1, fish2)
                #  print(f"changed={changed} index1={index1} index2={index2}")
                #  self.fishes[index1] = fish1
                #  self.fishes[index2] = fish2


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
        mgr.collisions()
        mgr.draw()
        pg.display.flip()
    pg.quit


main()
