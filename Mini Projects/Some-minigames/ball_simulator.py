import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import sys
import math
import pygame as pg

FPS = 1000
WIDTH = 1080
HEIGHT = 720
GRAVITY = 18

MOUSE_COLOR = "red"
PATH_COLOR = "purple"

LINE_COLOR = "black"
LINE_RADIUS = 2

BALL_COLOR = "black"
BALL_RADIUS = 12
BALL_INITIAL_X = WIDTH / 2
BALL_INITIAL_Y = HEIGHT - BALL_RADIUS - 1
BALL_SPEED_MULTIPLIER = 1.5

class Ball:
    def __init__(self, screen, current_ball_pos: tuple):
        self.screen = screen
        self.pos = current_ball_pos
    
    def draw_ball(self):
        pg.draw.circle(surface=self.screen, color=BALL_COLOR, center=self.pos, radius=BALL_RADIUS)
    
    def draw_line(self, end_pos):
        pg.draw.circle(surface=self.screen, color=MOUSE_COLOR, center=end_pos, radius=LINE_RADIUS)
        pg.draw.line(surface=self.screen, color=LINE_COLOR, start_pos=self.pos, end_pos=end_pos)
    
    def draw_ball_path(self, lst):
        if lst:
            for pix in lst:
                pg.draw.circle(surface=self.screen, color=PATH_COLOR, center=pix, radius=LINE_RADIUS)

    def update(self, current_ball_pos, draw=True):
        self.pos = current_ball_pos
        if draw:
            self.draw_ball()
    
    def calculate_angle(self, end_pos):
        x1, y1, x2, y2 = [*self.pos, *end_pos]

        angle = 90 if x1 - x2 == 0 else math.atan(abs(y1 - y2) / -(x1 - x2)) * 180 / math.pi
        return angle
    
    def launch(self, press_time, current_mouse_pos, acceleration_time=BALL_SPEED_MULTIPLIER):
        angle = self.calculate_angle(current_mouse_pos)
        angle = 180 + angle if angle < 0 else angle

        start_time = pg.time.get_ticks()
        acceleration = press_time * 100
        start_velocity_x = -acceleration_time * acceleration * math.cos(math.radians(angle))
        start_velocity_y = abs(acceleration_time * acceleration * math.sin(math.radians(angle)))
        
        return start_time, start_velocity_x, start_velocity_y

def run():

    def exit():
        pg.display.quit()
        pg.quit()
        sys.exit()

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    current_ball_pos = (BALL_INITIAL_X, BALL_INITIAL_Y)
    current_mouse_pos = None
    launch = False
    ball_path_list = []

    ball = Ball(screen, current_ball_pos)

    while 1:
        screen.fill((255, 255, 255))

        if launch:
            time_passed = (pg.time.get_ticks() - start_time) / 1000.0 * 8
            if current_ball_pos[1] <= BALL_INITIAL_Y:
                x, y = start_ball_pos
                change_x = start_velocity_x * time_passed
                change_y = start_velocity_y * time_passed - 0.5 * GRAVITY * pow(time_passed, 2)
                current_ball_pos = (x - change_x, y - change_y)
                ball_path_list.append(current_ball_pos)
            else:
                launch = False
                current_ball_pos = (current_ball_pos[0], BALL_INITIAL_Y)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEMOTION:
                current_mouse_pos = event.pos
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    launch = False
                    current_ball_pos = (BALL_INITIAL_X, BALL_INITIAL_Y)
                elif event.key == pg.K_q:
                    exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                start_count_time = pg.time.get_ticks()
            elif event.type == pg.MOUSEBUTTONUP and not launch:
                start_time, start_velocity_x, start_velocity_y = \
                    ball.launch((pg.time.get_ticks() - start_count_time) / 1000.0, current_mouse_pos)
                start_ball_pos = current_ball_pos
                ball_path_list = []
                launch = True
                
        ball.draw_ball_path(ball_path_list)
        ball.update(current_ball_pos)

        # draw the line connecting from ball to mouse
        if current_mouse_pos is not None:
            ball.draw_line(current_mouse_pos)

        clock.tick(FPS)
        pg.display.update()

if __name__ == '__main__':
    run()