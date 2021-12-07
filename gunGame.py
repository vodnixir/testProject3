import pygame as pg
import numpy as np

FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TURQUOISE = (48, 213, 200)
BACKGROUND = TURQUOISE
SCREEN_WIDTH = 800
SCREEN_HIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HIGHT)
GUN_COLOR = RED
DOT_COLOR = YELLOW


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
        self.new_mission()

    def new_mission(self):
        pass

    def process(self, events, screen):
        done = self.handle_events(events)
        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)
        self.move()
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
            elif event.type == pg.MOUSEBUTTONDOWN:
                print(f"Mouse {event.button} down")
            elif event.type == pg.MOUSEBUTTONUP:
                print(f"Mouse {event.button} UP")
        return done

    def move(self):
        pass

    def collide(self):
        pass

    def draw(self, screen):
        self.gun.draw(screen)


class GameObject:
    pass


class Cannon(GameObject):
    def __init__(self, coord=None, angle=None, max_pow=125, min_pow=75, color=GUN_COLOR, dot_color=DOT_COLOR):
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
    def set_angle(self,target_pos):
        # пушка
        # self.angle = np.arctan2(target_pos[1] - self.coord[1],target_pos[0] - self.coord[0])
        # лук
        self.angle = np.arctan2(-(target_pos[1] - self.coord[1]), -(target_pos[0] - self.coord[0]))
    def activate(self):
        self.active = True

    def draw(self, screen):
        gun_pos = np.array(self.coord)
        vec_2 = np.array([int(self.pow * np.cos(self.angle)), int(self.pow * np.sin(self.angle))])
        # только линия
        # pg.draw.line(screen, self.color, gun_pos.tolist(), (gun_pos + vec_2).tolist())
        # большой круг с маленьким
        pg.draw.circle(screen, self.color, gun_pos.tolist(), self.pow,1)
        pg.draw.circle(screen, self.dot_color, (gun_pos + vec_2).tolist(), self.pow // 10)
        pg.draw.line(screen, self.color, gun_pos.tolist(), (gun_pos + vec_2).tolist())

main()
