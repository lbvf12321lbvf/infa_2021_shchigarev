import pygame
from pygame.draw import *

pygame.init()


def cat(x1, y1, x2, y2, colorc, colory):
    a = y2 - y1
    b = x2 - x1
    if b >= 0:
        ellipse(sc, colorc,
                (x1 + b / 20, y1 + a / 2, b / 8, a / 2))  # 1 нога
        ellipse(sc, WHITE,
                (x1 + b / 20, y1 + a / 2, b / 8, a / 2), 2)
        ellipse(sc, colorc,
                (x1 + b * 7 / 8, y1 + a / 2, b / 3, a / 3))  # хвост
        ellipse(sc, WHITE,
                (x1 + b * 7 / 8, y1 + a / 2, b / 3, a / 3), 2)
        ellipse(sc, colorc,
                (x1 + b / 8, y1 + 1 / 5 * a, 5 * b / 6, a * 4 / 5))  # тело
        ellipse(sc, WHITE,
                (x1 + b / 8, y1 + 1 / 5 * a, 5 * b / 6, a * 4 / 5), 2)
        circle(sc, colorc,
               (x1 + b / 6, y1 + a / 2), a / 3)  # голова
        circle(sc, WHITE,
               (x1 + b / 6, y1 + a / 2), a / 3, 2)
        ellipse(sc, colorc,
                (x1 + b / 6, y1 + a * 6 / 7, b / 5, a / 5))  # 2 ног
        ellipse(sc, WHITE,
                (x1 + b / 6, y1 + a * 6 / 7, b / 5, a / 5), 2)
        circle(sc, colorc,
               (x1 + 5 * b / 6, y1 + 4 / 5 * a), a / 4)  # круг ноги 3
        circle(sc, WHITE,
               (x1 + 5 * b / 6, y1 + 4 / 5 * a), a / 4, 2)
        ellipse(sc, colorc,
                (x1 + b * 7 / 8, y1 + a * 7 / 8, b / 8, a / 3))
        ellipse(sc, WHITE,
                (x1 + b * 7 / 8, y1 + a * 7 / 8, b / 8, a / 3), 2)  # нога 3

        circle(sc, colory,
               (x1 + b / 6 + b / 15, y1 + a / 2 - a / 10), a / 14)  # глаза
        circle(sc, colory,
               (x1 + b / 6 - b / 15, y1 + a / 2 - a / 10), a / 14)
        circle(sc, BLACK,
               (x1 + b / 6 + b / 15, y1 + a / 2 - a / 10), a / 14, 1)
        circle(sc, BLACK,
               (x1 + b / 6 - b / 15, y1 + a / 2 - a / 10), a / 14, 1)
        ellipse(sc, BLACK,
                (x1 + b / 6 + b / 15 + b / 100, y1 + a / 2 - a / 10 - a / 20, b / 100, a / 10))
        ellipse(sc, BLACK,
                (x1 + b / 6 - b / 15 + b / 100, y1 + a / 2 - a / 10 - a / 20, b / 100, a / 10))
    else:
        ellipse(sc, colorc,
                (x1 + b / 20, y1 + a / 2, b / 8, a / 2))  # 1 нога
        ellipse(sc, colorc,
                (x1 + b * 7 / 8, y1 + a / 2, b / 3, a / 3))  # хвост
        ellipse(sc, colorc,
                (x1 + b / 8, y1 + 1 / 5 * a, 5 * b / 6, a * 4 / 5))  # тело
        circle(sc, colorc,
               (x1 + b / 6, y1 + a / 2), a / 3)  # голова
        ellipse(sc, colorc,
                (x1 + b / 6, y1 + a * 6 / 7, b / 5, a / 5))  # 2 ног
        circle(sc, colorc,
               (x1 + 5 * b / 6, y1 + 4 / 5 * a), a / 4)  # круг ноги 3
        circle(sc, WHITE,
               (x1 + 5 * b / 6, y1 + 4 / 5 * a), a / 4, 2)
        ellipse(sc, colorc,
                (x1 + b * 7 / 8, y1 + a * 7 / 8, b / 8, a / 3))
        circle(sc, colory,
               (x1 + b / 6 + b / 15, y1 + a / 2 - a / 10), a / 14)  # глаза
        circle(sc, colory,
               (x1 + b / 6 - b / 15, y1 + a / 2 - a / 10), a / 14)
        circle(sc, BLACK,
               (x1 + b / 6 + b / 15, y1 + a / 2 - a / 10), a / 14, 1)
        circle(sc, BLACK,
               (x1 + b / 6 - b / 15, y1 + a / 2 - a / 10), a / 14, 1)
        ellipse(sc, BLACK,
                (x1 + b / 6 + b / 15 + b / 100, y1 + a / 2 - a / 10 - a / 20, b / 100, a / 10))
        ellipse(sc, BLACK,
                (x1 + b / 6 - b / 15 + b / 100, y1 + a / 2 - a / 10 - a / 20, b / 100, a / 10))
    pygame.draw.polygon(sc, WHITE,
                        [(x1 + (0.316 * b) * 2 / 3, y1 + 0.19 * a), (x1 + (0.44 * b) * 2 / 3, y1 + 0.314 * a),
                         (x1 + (0.45 * b) * 2 / 3, y1 + 0.1 * a)], 4)  # уши
    pygame.draw.polygon(sc, colorc,
                        [(x1 + (0.316 * b) * 2 / 3, y1 + 0.19 * a), (x1 + (0.44 * b) * 2 / 3, y1 + 0.314 * a),
                         (x1 + (0.45 * b) * 2 / 3, y1 + 0.1 * a)])
    pygame.draw.polygon(sc, WHITE,
                        [(x1 + b / 10, y1 + 0.19 * a), (x1 - (0.12 * b) * 2 / 3 + b / 10, y1 + 0.314 * a),
                         (x1 - (0.17 * b) * 2 / 3 + b / 10, y1 + 0.1 * a)], 5)
    pygame.draw.polygon(sc, colorc,
                        [(x1 + b / 10, y1 + 0.19 * a), (x1 - (0.12 * b) * 2 / 3 + b / 10, y1 + 0.314 * a),
                         (x1 - (0.17 * b) * 2 / 3 + b / 10, y1 + 0.1 * a)])
    pygame.draw.polygon(sc, WHITE,
                        [(x1 + b / 6 + b / 50, y1 + a / 2 - a / 50), (x1 + b / 6 - b / 50, y1 + a / 2 - a / 50),
                         (x1 + b / 6, y1 + a / 2)], 2)
    for i in range(5):
        pygame.draw.line(sc, WHITE, (x1 + b / 6 + b / 30, y1 + a / 2 + a / 20 + a / 50 * i),
                         (x1 + b / 6 + b / 4, y1 + a / 2 - a / 30 + a / 20 + a / 35 * i), 1)  # усы
        pygame.draw.line(sc, WHITE, (x1 + b / 6 - b / 30, y1 + a / 2 + a / 20 + a / 50 * i),
                         (x1 + b / 6 - b / 4, y1 + a / 2 - a / 30 + a / 20 + a / 35 * i), 1)
        ellipse(sc, WHITE,
                (x1 + b / 6, y1 + a / 2, 2, a / 8), 2)


def klu(x1, y1, colk, r, napr):
    circle(sc, colk, (x1, y1), r)
    circle(sc, WHITE, (x1, y1), r, 2)
    for i in range(3):
        pygame.draw.line(sc, WHITE, (x1, y1 - 4 / 5 * r + i * r / 4), (x1 + r / 4 + i * r / 4, y1 - r / 2 + i * r / 4))
        pygame.draw.line(sc, WHITE, (x1 - r / 2, y1 + r / 2 - r / 4 * i), (x1 + r / 3, y1 + r * 2 / 3 - r / 5 * i))
    pygame.draw.lines(sc, WHITE, False, [(x1 + 1.41 / 2 * r * napr, y1 + 1.41 / 2 * r), (x1 + r * napr, y1 + r),
                                         (x1 + (1.41 / 2 + 1) * r * napr, y1 + 1.41 / 2 * r),
                                         (x1 + 2 * r * napr, y1 + r)])


def wn(x1, y1, a, b):
    pygame.draw.polygon(sc, LIGHT_BLUE, [(x1, y1), (x1, y1 + b), (x1 + a, y1 + b), (x1 + a, y1)])
    pygame.draw.polygon(sc, BLUE, [(x1 + 1 / 13 * a, y1 + 1 / 13 * b), (x1 + 1 / 13 * a, y1 + 1 / 13 * b + 3 / 13 * b),
                                   (x1 + 1 / 13 * a + a * 5 / 13, y1 + 1 / 13 * b + 3 / 13 * b),
                                   (x1 + 1 / 13 * a + a * 5 / 13, y1 + 1 / 13 * b)])
    pygame.draw.polygon(sc, BLUE, [(x1 + 7 / 13 * a, y1 + 1 / 13 * b), (x1 + 7 / 13 * a, y1 + 1 / 13 * b + 3 / 13 * b),
                                   (x1 + 7 / 13 * a + a * 5 / 13, y1 + 1 / 13 * b + 3 / 13 * b),
                                   (x1 + 7 / 13 * a + a * 5 / 13, y1 + 1 / 13 * b)])
    pygame.draw.polygon(sc, BLUE, [(x1 + 1 / 13 * a, y1 + 5 / 13 * b), (x1 + 1 / 13 * a, y1 + 5 / 13 * b + 7 / 13 * b),
                                   (x1 + 1 / 13 * a + a * 5 / 13, y1 + 5 / 13 * b + 7 / 13 * b),
                                   (x1 + 1 / 13 * a + a * 5 / 13, y1 + 5 / 13 * b)])
    pygame.draw.polygon(sc, BLUE, [(x1 + 7 / 13 * a, y1 + 5 / 13 * b), (x1 + 7 / 13 * a, y1 + 5 / 13 * b + 7 / 13 * b),
                                   (x1 + 7 / 13 * a + a * 5 / 13, y1 + 5 / 13 * b + 7 / 13 * b),
                                   (x1 + 7 / 13 * a + a * 5 / 13, y1 + 5 / 13 * b)])


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (204, 229, 252)
BLUE = (50, 148, 240)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
RED = (255, 0, 0)
STENA = (134, 77, 28)
POL = (134, 153, 28)
LAS = (40, 171, 215)
pi = 3.1415
FPS = 30
sc = pygame.display.set_mode((700, 700))
pygame.draw.polygon(sc, STENA, [(0, 0), (0, 300), (700, 300), (700, 0)])
pygame.draw.polygon(sc, POL, [(0, 300), (0, 700), (700, 700), (700, 300)])

cat(300, 300, 500, 400, GRAY, GREEN)
cat(500, 300, 600, 350, GRAY, GREEN)
cat(100, 600, 300, 700, GRAY, GREEN)
cat(300, 300, 100, 400, RED, PINK)
cat(500, 500, 400, 550, RED, PINK)

klu(400, 400, GREEN, 30, -1)
klu(650, 400, GREEN, 20, 1)
klu(200, 450, GREEN, 30, -1)
klu(100, 550, GREEN, 30, 1)
klu(600, 600, GREEN, 60, -1)

wn(100, 50, -200, 200)
wn(400, 50, -200, 200)
wn(650, 50, -200, 200)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
