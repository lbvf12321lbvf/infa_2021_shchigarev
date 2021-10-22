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
    if event.keysym == 'a':
        vx = -5
    elif event.keysym == 'd':
        vx = 5
    elif event.keysym == 'w':
        vy = -5
    elif event.keysym == 's':
        vy = 5
    if event.keysym == '1' or '2':
        g1.shoot_type(event.keysym)


def on_key_release(event):
    global vx, vy
    if event.keysym in ('a', 'd'):
        vx = 0
    elif event.keysym in ('w', 's'):
        vy = 0


class board():
    def __init__(self, x, y, hx, hy):
        self.x = x
        self.y = y
        self.hx = hx
        self.hy = hy
        self.k = 1
        self.id = canv.create_line(x, y, x + hx, y + hy, width=2)
        self.kx = 1

    def check(self, obj, typ=''):
        y = obj.y
        x = obj.x
        r = obj.r
        if isinstance(obj, ball):
            self.k = 3 / 4
        if isinstance(obj, target):
            if obj.type == 'carier':
                self.kx = 2

        if self.hy == 0:
            if (self.y + r) >= y and (self.y - r) <= y and self.x < x and self.x + self.hx > x:
                obj.y = self.y + (r + 1) * np.sign(obj.vy)
                obj.vy = - obj.vy * self.k
                obj.vx *= self.k
        if self.hx == 0:
            if (self.x + r * self.kx) >= x and (self.x - r * self.kx) <= x and self.y < y and self.y + self.hy > y:
                obj.x = self.x - (r * self.kx + 1) * np.sign(obj.vx)
                obj.vx = - obj.vx * self.k
                obj.vy *= self.k
        if obj.x >= 1000 or obj.y >= 1000 or obj.y <= -100 or obj.y <= -100:
            obj.live = - 1
        self.k = 1
        self.kx = 1


class ball():
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
        self.vx = self.vx * math.cos(fi) + self.vy * math.sin(fi)
        self.vy = - self.vx * math.sin(fi) + self.vy * math.cos(fi)

    def set_coords(self):
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

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

        if abs(obj.x - self.x) <= (self.r + obj.r) and abs(obj.y - self.y) <= (self.r + obj.r) and obj.live == 1:
            return True
        else:
            return False


class gun():
    def __init__(self):
        self.f2_power = 5
        self.type = 'ball'
        self.f2_on = 0
        self.an = 1
        self.ou = 1
        self.vx = 0
        self.vy = 0
        self.r = 5
        self.x = 20
        self.y = 450
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_line(20, 450, 50, 420, width=7)
        self.id2 = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )

    def shoot_type(self, x):
        if x == '1':
            self.type = 'ball'
            print(1)
        if x == '2':
            self.type = 'shootgan'
            print(2)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        if self.type == 'ball':
            new_ball = ball(self.x, self.y)
            new_ball.r += 5
            if (event.x - self.x) >= 0:
                self.an = math.atan((event.y - self.y) / (event.x - self.x))
            else:
                self.an = - math.atan((event.y - self.y) / (event.x - self.x))
            if (event.x - self.x) >= 0:
                new_ball.vx = self.f2_power * math.cos(self.an)
                new_ball.vy = - self.f2_power * math.sin(self.an)
            else:
                new_ball.vx = - self.f2_power * math.cos(self.an)
                new_ball.vy = - self.f2_power * math.sin(self.an)
            balls += [new_ball]
            self.f2_on = 0
            self.f2_power = 10
        if self.type == 'shootgan':
            for i in range(3):
                new_ball = ball(self.x, self.y)
                new_ball.r -= 2
                if (event.x - self.x) >= 0:
                    self.an = math.atan((event.y - self.y) / (event.x - self.x))
                else:
                    self.an = - math.atan((event.y - self.y) / (event.x - self.x))
                if (event.x - self.x) >= 0:
                    new_ball.vx = self.f2_power * math.cos(self.an)
                    new_ball.vy = - self.f2_power * math.sin(self.an)
                else:
                    new_ball.vx = - self.f2_power * math.cos(self.an)
                    new_ball.vy = - self.f2_power * math.sin(self.an)
                new_ball.rot(-0.3 + 0.3 * i)
                balls += [new_ball]

            self.f2_on = 0
            self.f2_power = 10

    def targetting(self, event=0):
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
                            self.x + max(self.f2_power, 20) * math.cos(self.an),
                            self.y + max(self.f2_power, 20) * math.sin(self.an)
                            )
            else:
                canv.coords(self.id, self.x, self.y,
                            self.x - max(self.f2_power, 20) * math.cos(self.an),
                            self.y + max(self.f2_power, 20) * math.sin(self.an)
                            )
        else:
            if self.ou == 1:
                canv.coords(self.id, self.x, self.y,
                            self.x + max(self.f2_power, 20) * math.cos(self.an),
                            self.y + max(self.f2_power, 20) * math.sin(self.an)
                            )
            else:
                canv.coords(self.id, self.x, self.y,
                            self.x - max(self.f2_power, 20) * math.cos(self.an),
                            self.y + max(self.f2_power, 20) * math.sin(self.an)
                            )

        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')

    def move(self, vx, vy):
        self.vx = vx
        self.vy = -vy
        self.x += vx
        self.y += vy
        canv.coords(
            self.id2,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )
        for bord in boards:
            bord.check(self)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 50:
                self.f2_power += 0.5
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class target():
    def __init__(self, typ='standart'):
        self.points = 0
        self.live = 1
        self.type = typ
        if self.type == 'standart' or self.type == 'carier':
            self.id = canv.create_oval(0, 0, 0, 0)
        elif self.type == 'rare':
            self.id = canv.create_rectangle(0, 0, 0, 0)
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        if self.type == 'standart':
            x = self.x = rnd(600, 780)
            y = self.y = rnd(300, 550)
            r = self.r = rnd(7, 50)
            color = self.color = 'red'
            canv.coords(self.id, x - r, y - r, x + r, y + r)
            canv.itemconfig(self.id, fill=color)
            self.vy = rnd(-10, 10)
            self.vx = rnd(-10, 10)
        elif self.type == 'rare':
            x = self.x = rnd(600, 780)
            y = self.y = rnd(300, 550)
            r = self.r = rnd(7, 15)
            color = self.color = 'blue'
            canv.coords(self.id, x - r, y - r, x + r, y + r)
            canv.itemconfig(self.id, fill=color)
            self.vy = rnd(-15, 15)
            self.vx = rnd(-15, 15)
        elif self.type == 'carier':
            x = self.x = rnd(600, 780)
            y = self.y = rnd(300, 550)
            r = self.r = rnd(20, 30)
            color = self.color = 'green'
            canv.coords(self.id, x - 2 * r, y - r, x + 2 * r, y + r)
            canv.itemconfig(self.id, fill=color)
            self.vy = rnd(-5, 5)
            self.vx = rnd(-5, 5)

    def move(self, boards):
        for bord in boards:
            bord.check(self)
        self.x += self.vx
        self.y -= self.vy

        if self.live <= 0:
            canv.delete(self.id)
        else:
            self.set_coords()

    def set_coords(self):
        if self.type != 'carier':
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
        self.points += points
        if self.type == 'rare':
            self.points += 2 * points
        canv.delete(self.id)

    def dele(self):
        canv.delete(self.id)


class texty():
    def __init__(self):
        self.id = canv.create_text(30, 30, text='', font='28')

    def peretext(self, sc):
        canv.delete(self.id)
        self.id = canv.create_text(30, 30, text=str(sc), font='28')


t1 = defaultdict(lambda: '')
tr = defaultdict(lambda: '')
tc = defaultdict(lambda: '')
screen1 = canv.create_text(400, 300, text='', font='28')
g1 = gun()
bullet = 0
score = 0
vx = 0
vy = 0
balls = []
t1[0] = target()
t1[0].dele()

tx = texty()
boards = []
boards.append(board(4, 4, 800, 0))
boards.append(board(4, 596, 800, 0))
boards.append(board(4, 4, 0, 600))
boards.append(board(796, 4, 0, 600))
boards.append(board(300, 4, 0, 200))
boards.append(board(500, 400, 0, 200))


def new_game(N, event=''):
    global gun, t1, screen1, balls, bullet, score
    for i in range(N):
        t1[i + 1] = target()
        t1[i + 1].new_target()
    for i in range(N - 1):
        tr[i] = target(typ='rare')
        tr[i].new_target()
    for i in range(N - 1):
        tc[i] = target(typ='carier')
        tc[i].new_target()
    bullet = 0
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    canv.bind('<Motion>', g1.targetting)
    canv.bind('<Motion>', g1.targetting)
    root.bind('<KeyPress>', on_key_press)
    root.bind('<KeyRelease>', on_key_release)

    z = 0.01
    l = 0
    num = 0
    t1[0].live = 1
    while t1[0].live or balls:
        for b in balls:
            b.move(boards)
            for i in range(N):
                if b.hittest(t1[i + 1]):
                    t1[i + 1].live = 0
                    t1[i + 1].hit()
                    l += 1
            for i in range(N - 1):
                if b.hittest(tr[i]):
                    tr[i].live = 0
                    tr[i].hit()
                    l += 1
            for i in range(N - 1):
                if b.hittest(tc[i]):
                    tc[i].live = 0
                    tc[i].hit()
                    l += 1
            if l == 3 * N - 2 + num:
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen1, text='Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
                t1[0].live = 0
        score = 0
        for i in range(N):
            t1[i + 1].move(boards)
            score += t1[i + 1].points
        for i in range(N - 1):
            tr[i].move(boards)
            score += tr[i].points
        for i in range(N - 1):
            tc[i].move(boards)
            score += tc[i].points
        tx.peretext(score)
        canv.update()
        time.sleep(z)
        g1.move(vx, vy)
        g1.targetting()
        g1.power_up()
    canv.itemconfig(screen1, text='')
    canv.delete(gun)
    root.after(750, new_game(N + 1))


new_game(1)

root.mainloop()
