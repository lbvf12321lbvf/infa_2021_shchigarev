import pygame
from pygame.draw import *
from random import randint
from collections import defaultdict
from math import sqrt
from time import sleep
from math import sin
from random import random


def new_ball(x, y, r, color):
    """
    рисует новый шарик
    """
    circle(screen, color, (x, y), r)


def new_spyk(x, y, r, color):
    """
    рисует спику
    """
    rect(screen, color,
         (x - r, y - r, 2 * r, 2 * r))


def snyp(pos):
    """
    проверяет попал ли клик в какой-либо шар или пику
    :param pos: координаты клика
    :return: 1 если попал в шарик, 0 если нет 2 если в спику
    """
    x, y = pos
    for item in balls:
        if sqrt((item[1] - x) ** 2 + (item[2] - y) ** 2) <= item[3]:
            balls[item[0]][3] = 0
            return 1
    for item in spyk:
        if abs(item[1] - x) <= spyk[i][3] and + abs(item[2] - y) <= item[3]:
            spyk[item[0]][3] = 0
            return 2
    return 0


def gen_balls(k):
    """
    создаёт массив шаров 0 номер шара, 1 хшара 2 у шара 3- радиус 4 - цвет шара
    :param k: количество шаров
    :return: массив шаров
    """
    return [[int(s), randint(100, Xsc - 100), randint(100, Ysc - 100), randint(25, 40), COLORS[randint(1, 5)]] for s in
            range(k)]


def gen_spyk(k):
    """
    создаёт массив  быстрых пик 0 номер пики, 1 хпики 2 у пики 3- радиус 4 - vx 5 -vy 6 - цвет 7 - фаза x 8 - фаза y
    :param k: количество пик
    :return: массив пик
    """

    return [
        [int(s), randint(100, Xsc - 100), randint(100, Ysc - 100), randint(15, 20), randint(-10, 10), randint(-10, 10),
         RED, int(int(random()) * 3.14), int(int(random()) * 3.14)] for s in
        range(k)]


with open('C:\\Users\\dimas\\Desktop\\Лидеры.txt', 'r') as tt:
    ms = tt.readlines()
    mas = [["", 1] for s in range(len(ms) + 1)]
    for i in range(len(ms)):
        mas[i][0] = str(ms[i].split()[:-1][0])
        mas[i][1] = int(ms[i].split()[-1:][0])

print('Enter your name:')
name = input()

Xsc = 1000
Ysc = 650
FPS = 50
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
N = 7
n = 0
score = 0
time = 2
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

vx = defaultdict(lambda: randint(-10, 10))
vy = defaultdict(lambda: randint(-10, 10))

balls = gen_balls(N)
spyk = gen_spyk(N - 5)

pygame.init()
screen = pygame.display.set_mode((Xsc, Ysc))
score_font = pygame.font.SysFont("", 30)
time_font = pygame.font.SysFont("", 30)
score_texture = score_font.render('', False, (0, 0, 0))
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    time = time - 1 / FPS
    if time <= 0:
        screen.blit(score_texture, (Xsc / 2 - score_texture.get_width() / 2, Ysc / 2 - 15))
        for i in range(len(balls)):
            balls[i][3] = 0
        pygame.display.update()
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            realy = snyp(event.pos)
            if realy == 1:
                print("Попал!")
                n += 1
                score += 1
            elif realy == 2:
                print("Круто попал!")
                n += 1
                score += 3
        if n == 2 * N - 5:
            N = n + 1
            n = 0
            score += 5
            balls = gen_balls(N)
            spyk = gen_spyk(N - 5)
    for i in range(len(balls)):
        # Перемещение шаров
        balls[i][1] += vx[balls[i][0]]
        balls[i][2] += vy[balls[i][0]]
        new_ball(balls[i][1], balls[i][2], balls[i][3], balls[i][4])
        # Отражения шаров
        if balls[i][1] - balls[i][3] <= 0:
            vx[balls[i][0]] = abs(vx[balls[i][0]])
        elif balls[i][2] - balls[i][3] <= 0:
            vy[balls[i][0]] = abs(vy[balls[i][0]])
        elif balls[i][1] + balls[i][3] >= Xsc:
            vx[balls[i][0]] = -abs(vx[balls[i][0]])
        elif balls[i][2] + balls[i][3] >= Ysc:
            vy[balls[i][0]] = -abs(vy[balls[i][0]])
    for i in range(len(spyk)):
        # Перемещение пик
        spyk[i][1] += spyk[i][4] * 1 / 2 + sin(time * 5 + spyk[i][7]) * abs(spyk[i][5])
        spyk[i][2] += spyk[i][5] * 1 / 2 + sin(time * 5 + spyk[i][8]) * abs(spyk[i][4])
        new_spyk(spyk[i][1], spyk[i][2], spyk[i][3], spyk[i][6])
        # Отражения пик
        if spyk[i][1] - spyk[i][3] <= 0:
            spyk[i][4] = abs(spyk[i][4])
        elif spyk[i][2] - spyk[i][3] <= 0:
            spyk[i][5] = abs(spyk[i][5])
        elif spyk[i][1] + spyk[i][3] >= Xsc:
            spyk[i][4] = -abs(spyk[i][4])
        elif spyk[i][2] + spyk[i][3] >= Ysc:
            spyk[i][5] = -abs(spyk[i][5])

    score_texture = score_font.render('Your score: ' + str(score), False, (220, 225, 20))
    time_texture = time_font.render('Time left: ' + str(round(time, 1)), False, (220, 225, 20))

    screen.blit(score_texture, (0, 0))
    screen.blit(time_texture, (Xsc - 200, 0))

    pygame.display.update()
    screen.fill(BLACK)


mas[len(ms)][0] = str(name) + str(':score:')
mas[len(ms)][1] = score

Mas = sorted(mas, key=lambda x: x[1], reverse=True)
lines = [str(Mas[s][0]) + ' ' + str(Mas[s][1]) + '\n' for s in range(len(ms) + 1)]

with open('C:\\Users\\dimas\\Desktop\\Лидеры.txt', 'w') as tt:
    tt.writelines(lines)

sleep(2)

pygame.quit()
