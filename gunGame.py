import pygame as pg
from random import randint
import numpy as np
import datetime as dt

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TURQUOISE = (48, 213, 200)
BACKGROUND = TURQUOISE
SCREEN_WIDTH = 1600
SCREEN_HIGHT = 1200
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HIGHT)
GUN_COLOR = RED
DOT_COLOR = YELLOW
AUTO_MOVE_NONE = 0
AUTO_MOVE_UP = 1
AUTO_MOVE_DOWN = 2
AUTO_MOVE_LEFT= 3
AUTO_MOVE_RIGHT = 4

CANON_SPEED = 360  # pixels per second


def rand_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))


def main():
    pg.init()
    pg.font.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption("GunGame")
    done = False
    clock = pg.time.Clock()
    mgr = GameManager()
    while not done:
        clock.tick(FPS)
        screen.fill(BACKGROUND)
        done = mgr.process(pg.event.get(), screen)
        pg.display.flip()
    pg.quit


class GameManager:
    def __init__(self):
        self.gun = Cannon()
        self.bullets = []
        self.new_mission()

    def new_mission(self):
        pass

    def process(self, events, screen):
        done = self.handle_events(events)
        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)
        self.update()
        self.collide()
        self.draw(screen)
        return done

    def handle_events(self, events):
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                print(f"Key={event.key}")
                if event.key == pg.K_s:
                    # self.gun.move(-5)
                    self.gun.auto_move_y = AUTO_MOVE_DOWN
                if event.key == pg.K_w:
                    # self.gun.move(5)
                    self.gun.auto_move_y = AUTO_MOVE_UP
                if event.key == pg.K_d:
                    # self.gun.move(-5)
                    self.gun.auto_move_x = AUTO_MOVE_LEFT
                if event.key == pg.K_a:
                    # self.gun.move(5)
                    self.gun.auto_move_x = AUTO_MOVE_RIGHT

            elif event.type == pg.KEYUP:
                if event.key == pg.K_s:
                    self.gun.auto_move_y = AUTO_MOVE_NONE
                elif event.key == pg.K_w:
                    self.gun.auto_move_y = AUTO_MOVE_NONE
                if event.key == pg.K_a:
                    self.gun.auto_move_x = AUTO_MOVE_NONE
                elif event.key == pg.K_d:
                    self.gun.auto_move_x = AUTO_MOVE_NONE
            elif event.type == pg.MOUSEBUTTONDOWN:
                # print(f"Mouse {event.button} down")
                if event.button == 1:
                    self.gun.active = True
            elif event.type == pg.MOUSEBUTTONUP:
                # print(f"Mouse {event.button} UP")
                if event.button == 1:
                    bullet = self.gun.shoot()
                    self.bullets.append(bullet)
        return done

    def update(self):
        self.gun.update()
        dead_bullets = []
        for i, bullet in enumerate(self.bullets):
            bullet.move(time=1, grav=2)
            if not bullet.is_alive:
                dead_bullets.append(i)
        for i in reversed(dead_bullets):
            self.bullets.pop(i)

    def collide(self):
        pass

    def draw(self, screen):
        self.gun.draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)


class GameObject:
    pass


class Cannon(GameObject):
    def __init__(self, coord=None, angle=None, max_pow=125, min_pow=25, color=GUN_COLOR, dot_color=DOT_COLOR):
        if coord is None:
            coord = [SCREEN_WIDTH // 2, SCREEN_HIGHT // 2]
        self.coord = coord
        if angle is None:
            angle = (-45 * np.pi) / 180
        self.angle = angle
        self.max_pow = max_pow
        self.min_pow = min_pow
        self.color = color
        self.dot_color = dot_color
        self.active = False
        self.pow = min_pow
        self.auto_move_x = AUTO_MOVE_NONE
        self.auto_move_y = AUTO_MOVE_NONE

    def set_angle(self, target_pos):
        # пушка
        self.angle = np.arctan2(target_pos[1] - self.coord[1], target_pos[0] - self.coord[0])
        # лук
        # self.angle = np.arctan2(-(target_pos[1] - self.coord[1]), -(target_pos[0] - self.coord[0]))

    def draw(self, screen):
        gun_pos = np.array(self.coord)
        vec_2 = np.array([int(self.pow * np.cos(self.angle)), int(self.pow * np.sin(self.angle))])
        # только линия
        # pg.draw.line(screen, self.color, gun_pos.tolist(), (gun_pos + vec_2).tolist())
        # большой круг с маленьким
        pg.draw.circle(screen, self.color, gun_pos.tolist(), self.pow, 1)
        pg.draw.circle(screen, self.dot_color, (gun_pos + vec_2).tolist(), self.pow // 10)
        pg.draw.line(screen, self.color, gun_pos.tolist(), (gun_pos + vec_2).tolist())

    def move(self, deltaX, deltaY):
        self.coord[1] += deltaY
        self.coord[0] += deltaX

    def update(self):
        if self.auto_move_y == AUTO_MOVE_UP:
            self.move(0,-CANON_SPEED // FPS)
        elif self.auto_move_y == AUTO_MOVE_DOWN:
            self.move(0,CANON_SPEED // FPS)
        if self.auto_move_x == AUTO_MOVE_RIGHT:
            self.move(-CANON_SPEED // FPS,0)
        elif self.auto_move_x == AUTO_MOVE_LEFT:
            self.move(CANON_SPEED // FPS,0)
        if self.active:
            self.pow += 5
            if self.pow > self.max_pow:
                self.pow = self.max_pow

    def shoot(self):
        vel = self.pow
        angle = self.angle
        gun_pos = np.array(self.coord)
        vec_2 = np.array([int(self.pow * np.cos(self.angle)), int(self.pow * np.sin(self.angle))])
        bullet = Bullet((gun_pos + vec_2).tolist(), [int(vel * np.cos(angle)), int(vel * np.sin(angle))])
        self.pow = self.min_pow
        self.active = False
        return bullet


class Bullet(GameObject):
    def __init__(self, coord, vel, rad=20, color=None):
        self.coord = coord
        self.vel = vel
        if color is None:
            color = rand_color()
        self.color = color
        self.rad = rad
        self.is_alive = True

    def check_corners(self, refl_ort=0.8, refl_par=0.9):
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1 - i] = int(self.vel[1 - i] * refl_par)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1 - i] = int(self.vel[1 - i] * refl_par)

    def move(self, time=1, grav=0):
        self.vel[1] += grav
        for i in range(2):
            self.coord[i] += time * self.vel[i]
        self.check_corners()
        if self.vel[0] ** 2 + self.vel[1] ** 2 < 2 ** 2 and self.coord[1] > SCREEN_SIZE[1] - 2 * self.rad:
            self.is_alive = False

    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.coord, self.rad)


main()
