from random import randrange as rnd, choice
import tkinter as tk
import math
import numpy as np
import time
from collections import defaultdict

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


def on_key_press(event):
    global vx, vy
    if event.keysym in ('a', 'ф', 'A', 'Ф'):
        vx = -5
    elif event.keysym in ('d', 'в', 'D', 'В'):
        vx = 5
    elif event.keysym in ('w', 'ц', 'W', 'Ц',):
        vy = -5
    elif event.keysym in ('s', 'ы', 'S', 'Ы'):
        vy = 5
    if event.keysym == '1' or '2':
        g1.shot_type(event.keysym)


def on_key_release(event):
    global vx, vy
    if event.keysym in ('a', 'd', 'ф', 'A', 'Ф', 'в', 'D', 'В'):
        vx = 0
    elif event.keysym in ('w', 's', 'ц', 'W', 'Ц', 'ы', 'S', 'Ы'):
        vy = 0


class Board:
    def __init__(self, x, y, hx, hy):
        self.x = x
        self.y = y
        self.hx = hx
        self.hy = hy
        self.k = 1
        self.id = canv.create_line(x, y, x + hx, y + hy, width=2)
        self.kx = 1

    def check(self, obj, typ=''):
        """
        Проверка на столкновение между объектом и стеной и смена направления движения шарика при оном
        """
        global successful_targets
        y = obj.y
        x = obj.x
        r = obj.r
        if isinstance(obj, Balls):
            self.k = 3 / 4
        if isinstance(obj, Target):
            if obj.type == 'carrier':
                self.kx = 2

        if self.hy == 0:
            if (self.y + r) >= y >= (self.y - r) and self.x < x < self.x + self.hx:
                obj.y = self.y + (r + 1) * np.sign(obj.vy)
                obj.vy = - obj.vy * self.k
                obj.vx *= self.k
        if self.hx == 0:
            if (self.x + r * self.kx) >= x >= (self.x - r * self.kx) and self.y < y < self.y + self.hy:
                obj.x = self.x - (r * self.kx + 1) * np.sign(obj.vx)
                obj.vx = - obj.vx * self.k
                obj.vy *= self.k
        if obj.x >= 1000 or obj.y >= 1000 or obj.y <= -100 or obj.y <= -100:
            if isinstance(obj, Target) and obj.live > 0:
                successful_targets += 1
                print('lol')
            obj.live = - 1
        self.k = 1
        self.kx = 1


class Balls:
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 30

    def rot(self, fi):
        """поворот вектора скорости шарика на угол фи"""
        self.vx = self.vx * math.cos(fi) + self.vy * math.sin(fi)
        self.vy = - self.vx * math.sin(fi) + self.vy * math.cos(fi)

    def set_coords(self):
        """
        установка координат
        """
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self, boards):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        self.x += self.vx
        self.y -= self.vy
        self.vy -= 0.5
        self.vy *= 0.99
        self.vx *= 0.99
        for bord in boards:
            bord.check(self, typ='ball')
        if self.vx ** 2 + self.vy ** 2 <= 3:
            if self.live < 0:
                balls.pop(balls.index(self))
                canv.delete(self.id)
            else:
                self.live -= 1
        if self.live < 0:
            balls.pop(balls.index(self))
            canv.delete(self.id)
        self.set_coords()

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

        if abs(obj.x - self.x) <= (self.r + obj.r) and abs(obj.y - self.y) <= (self.r + obj.r) and obj.live >= 1:
            return True
        else:
            return False


class Gun:
    def __init__(self):
        self.power = 5
        self.live = 3
        self.inviz_time = 0
        self.type = 'ball'
        self.on = 0
        self.an = 1
        self.ou = 1
        self.vx = 0
        self.vy = 0
        self.r = 5
        self.x = 20
        self.y = 450
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.color2 = self.color
        self.id = canv.create_line(20, 450, 50, 420, width=7)
        self.id2 = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )

    def minus_live(self):
        """
        уменьшение жизни при попадании
        """
        if self.inviz_time <= 0:
            self.live -= 1
            self.color = 'white'
            self.inviz_time = 100

    def shot_type(self, x):
        """
        смена типа снаряда
        """
        if x == '1':
            self.type = 'ball'
            print(1)
        if x == '2':
            self.type = 'shotgun'
            print(2)

    def fire2_start(self, event):
        self.on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        if self.type == 'ball':
            new_ball = Balls(self.x, self.y)
            new_ball.r += 5
            if (event.x - self.x) >= 0:
                self.an = math.atan((event.y - self.y) / (event.x - self.x))
            else:
                self.an = - math.atan((event.y - self.y) / (event.x - self.x))
            if (event.x - self.x) >= 0:
                new_ball.vx = self.power * math.cos(self.an)
                new_ball.vy = - self.power * math.sin(self.an)
            else:
                new_ball.vx = - self.power * math.cos(self.an)
                new_ball.vy = - self.power * math.sin(self.an)
            balls += [new_ball]
            self.on = 0
            self.power = 10
        if self.type == 'shotgun':
            for i in range(3):
                new_ball = Balls(self.x, self.y)
                new_ball.r -= 2
                if (event.x - self.x) >= 0:
                    self.an = math.atan((event.y - self.y) / (event.x - self.x))
                else:
                    self.an = - math.atan((event.y - self.y) / (event.x - self.x))
                if (event.x - self.x) >= 0:
                    new_ball.vx = self.power * math.cos(self.an)
                    new_ball.vy = - self.power * math.sin(self.an)
                else:
                    new_ball.vx = - self.power * math.cos(self.an)
                    new_ball.vy = - self.power * math.sin(self.an)
                new_ball.rot(-0.3 + 0.3 * i)
                balls += [new_ball]

            self.on = 0
            self.power = 10

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

        if abs(obj.x - self.x) <= (self.r + obj.r) and abs(obj.y - self.y) <= (self.r + obj.r) and obj.live >= 1:
            return True
        else:
            return False

    def targeting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if (event.x - self.x) >= 0:
                self.an = math.atan((event.y - self.y) / (event.x - self.x))
                self.ou = 1
            else:
                self.an = - math.atan((event.y - self.y) / (event.x - self.x))
                self.ou = -1
            if (event.x - self.x) >= 0:
                canv.coords(self.id, self.x, self.y,
                            self.x + max(self.power, 20) * math.cos(self.an),
                            self.y + max(self.power, 20) * math.sin(self.an)
                            )
            else:
                canv.coords(self.id, self.x, self.y,
                            self.x - max(self.power, 20) * math.cos(self.an),
                            self.y + max(self.power, 20) * math.sin(self.an)
                            )
        else:
            if self.ou == 1:
                canv.coords(self.id, self.x, self.y,
                            self.x + max(self.power, 20) * math.cos(self.an),
                            self.y + max(self.power, 20) * math.sin(self.an)
                            )
            else:
                canv.coords(self.id, self.x, self.y,
                            self.x - max(self.power, 20) * math.cos(self.an),
                            self.y + max(self.power, 20) * math.sin(self.an)
                            )

        if self.on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')

    def move(self, v_x, v_y):
        """
        происходит перемещение ракеты
        """
        self.vx = v_x
        self.vy = -v_y
        self.x += v_x
        self.y += v_y
        canv.coords(
            self.id2,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
        )
        for bord in boards:
            bord.check(self)

    def chek_color(self):
        """
        проверка, нужно ли менять цвет и смена цвета
        """
        self.inviz_time -= 1
        if self.inviz_time <= 0:
            self.color = self.color2
        canv.itemconfig(self.id2, fill=self.color)

    def power_up(self):
        """
        Увеличение мощности при зажатии клавиши
        """
        if self.on:
            if self.power < 50:
                self.power += 0.5
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class Target:
    def __init__(self, typ='standard'):
        self.points = 0
        self.live = 1
        self.type = typ
        self.tik = 100
        if self.type == 'standard' or self.type == 'carrier':
            self.id = canv.create_oval(0, 0, 0, 0)
        elif self.type == 'rare':
            self.id = canv.create_rectangle(0, 0, 0, 0)
        self.new_target()

    def move(self, boards):
        """
        перемещение цели
        """
        for bord in boards:
            bord.check(self)
        self.x += self.vx
        self.y -= self.vy

        if self.live <= 0:
            canv.delete(self.id)
        else:
            self.set_coords()

    def set_coords(self):
        """
        установка координат
        """
        if self.type != 'carrier':
            canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
            )
        else:
            canv.coords(
                self.id,
                self.x - 2 * self.r,
                self.y - self.r,
                self.x + 2 * self.r,
                self.y + self.r)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        self.points = points
        if self.type == 'rare':
            self.points = 3 * points
        canv.delete(self.id)

    def delete_new(self):
        """
        новая функция удаления
        """
        canv.delete(self.id)


class Target_s(Target):
    def __init__(self, typ='standard'):
        self.points = 0
        self.live = 1
        self.type = typ
        self.tik = 100
        self.id = canv.create_oval(0, 0, 0, 0)

        self.new_target()

    def new_target(self, x1=rnd(600, 759), y1=rnd(300, 550)):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 750)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(7, 50)
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)
        self.vy = rnd(-10, 10)
        self.vx = rnd(-10, 10)


class Target_r(Target):
    def __init__(self, typ='rare'):
        self.points = 0
        self.live = 1
        self.type = typ
        self.tik = 100
        self.id = canv.create_rectangle(0, 0, 0, 0)
        self.new_target()

    def new_target(self, x1=rnd(600, 759), y1=rnd(300, 550)):
        """ Инициализация новой цели. """
        x = self.x = x1
        y = self.y = y1
        r = self.r = rnd(7, 15)
        color = self.color = 'blue'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)
        self.vy = rnd(-15, 15)
        self.vx = rnd(-15, 15)


class Target_c(Target):
    def __init__(self, typ='carrier'):
        self.points = 0
        self.live = 1
        self.type = typ
        self.tik = 100
        self.id = canv.create_oval(0, 0, 0, 0)
        self.new_target()

    def new_target(self, x1=rnd(600, 759), y1=rnd(300, 550)):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 750)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(20, 30)
        color = self.color = 'green'
        canv.coords(self.id, x - 2 * r, y - r, x + 2 * r, y + r)
        canv.itemconfig(self.id, fill=color)
        self.vy = rnd(-5, 5)
        self.vx = rnd(-5, 5)

    def spawn(self, n):
        """
        спавн синего квадрата
        """
        global t_rare, num

        if self.live > 0 and self.tik <= 0:
            num += 1
            t_rare[n - 2 + num] = Target_r()
            t_rare[n - 2 + num].new_target(x1=self.x, y1=self.y)
            self.tik = 50
        self.tik -= 1


class Texts:
    def __init__(self, x=30, y=30, tex=''):
        self.id = canv.create_text(x, y, text=tex, font='28')

    def peretext(self, sc, x=30, y=30, tex=''):
        """
        создаёт текст в нужной точке
        """
        canv.delete(self.id)
        self.id = canv.create_text(x, y, text=(tex + str(sc)), font='28')


t_standard = defaultdict(lambda: Target_s())
t_rare = defaultdict(lambda: Target_r())
t_carrier = defaultdict(lambda: Target_c())
screen1 = canv.create_text(400, 300, text='', font='28')
g1 = Gun()
bullet = 0
score = 0
vx = 0
vy = 0
k = 2
tik = 100
balls = []
t_standard[0] = Target_s()
t_standard[0].delete_new()
successful_targets = 0
num = 0
tx = Texts()
tx_live = Texts(x=70, y=30, tex='live: 0')
boards = [Board(4, 4, 800, 0), Board(4, 596, 800, 0), Board(4, 4, 0, 600), Board(796, 4, 0, 600), Board(300, 4, 0, 200),
          Board(500, 400, 0, 200)]


def new_game(n):
    global t_standard, screen1, balls, bullet, score, successful_targets, num, tik, k
    for i in range(n):
        t_standard[i + 1] = Target_s()
        t_standard[i + 1].new_target()
    for i in range(n - 1):
        t_rare[i] = Target_r()
        t_rare[i].new_target()
    for i in range(n - 1):
        t_carrier[i] = Target_c()
        t_carrier[i].new_target()
    bullet = 0
    balls = []
    g1.live = 3
    k = 3

    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targeting)
    canv.bind('<Motion>', g1.targeting)
    canv.bind('<Motion>', g1.targeting)
    root.bind('<KeyPress>', on_key_press)
    root.bind('<KeyRelease>', on_key_release)

    tick = 0.01
    successful_targets = 0
    num = 0
    t_standard[0].live = 1
    while (t_standard[0].live or balls) and k > 0:
        for b in balls:
            b.move(boards)
            for i in range(n):
                if b.hit_test(t_standard[i + 1]):
                    t_standard[i + 1].live = 0
                    t_standard[i + 1].hit()
                    successful_targets += 1
            for i in range(n - 1 + num):
                if b.hit_test(t_rare[i]):
                    t_rare[i].live = 0
                    t_rare[i].hit()
                    successful_targets += 1
            for i in range(n - 1):
                if b.hit_test(t_carrier[i]):
                    t_carrier[i].live = 0
                    t_carrier[i].hit()
                    successful_targets += 1

            if successful_targets == 3 * n - 2 + num and n > 0:
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen1, text='Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
                t_standard[0].live = 0
        score = 0
        for i in range(n):
            t_standard[i + 1].move(boards)
            score += t_standard[i + 1].points
        for i in range(n - 1 + num):
            t_rare[i].move(boards)
            score += t_rare[i].points
        for i in range(n - 1):
            t_carrier[i].move(boards)
            score += t_carrier[i].points
            t_carrier[i].spawn(n)

        for i in range(n - 1 + num):
            if g1.hit_test(t_rare[i]):
                g1.minus_live()
        tx_live.peretext(x=70, y=30, sc=str(g1.live), tex='live:')
        if g1.live == 0:
            canv.itemconfig(screen1, text='you lose, score:' + str(score))
            for i in range(n):
                t_standard[i + 1].live = 0
                t_standard[i + 1].hit()

            for i in range(n - 1 + num):
                t_rare[i].live = 0
                t_rare[i].hit()

            for i in range(n - 1):
                t_carrier[i].live = 0
                t_carrier[i].hit()
            t_standard[0].live = 0
            n = 0
            canv.update()
            time.sleep(2)
        tx.peretext(score)
        canv.update()
        time.sleep(tick)
        g1.move(vx, vy)
        g1.targeting()
        g1.power_up()
        g1.chek_color()

    canv.itemconfig(screen1, text='')
    canv.delete(Gun)
    root.after(750, new_game(n + 1))


new_game(1)

root.mainloop()
