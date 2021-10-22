from random import randrange as rnd, choice
import tkinter as tk
import math
import time
from collections import defaultdict

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


def on_key_press(event):
    global vx, vy
    if event.keysym == 'Left':
        vx = -5
    elif event.keysym == 'Right':
        vx = 5
    elif event.keysym == 'Up':
        vy = -5
    elif event.keysym == 'Down':
        vy = 5


def on_key_release(event):
    global vx, vy
    if event.keysym in ('Left', 'Right'):
        vx = 0
    elif event.keysym in ('Up', 'Down'):
        vy = 0

class board():
    def __init__(self, x=800, y=600):
        pass
class ball():
    def __init__(self, x=40, y=450, ):
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

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        if self.y <= 500:
            self.vy -= 1
            self.y -= self.vy
            self.x += self.vx
            self.vx *= 0.99
        else:
            if self.vx ** 2 + self.vy ** 2 > 10:
                self.vy = -self.vy * 3 / 4
                self.vx = self.vx * 3 / 4
                self.y = 499
            if self.live < 0:
                balls.pop(balls.index(self))
                canv.delete(self.id)
            else:
                self.live -= 1
        if self.y <= 0 + self.r:
            self.y = 1 + self.r
            self.vy = - self.vy * 3 / 4
        if self.x > 780:
            self.vx = -self.vx * 3 / 4
            self.x = 779
        if self.x < 0 + self.r:
            self.vx = - self.vx * 3 / 4
            self.x = 1 + self.r
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
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.ou = 1
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


    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
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


    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        canv.coords(
            self.id2,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )


    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class target():
    def __init__(self, typ=0):
        self.points = 0
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        self.new_target()
        self.type = typ

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)
        self.vy = rnd(-10, 10)
        self.vx = rnd(-10, 10)

    def move(self):
        if self.y <= (500 - self.r):
            self.y -= self.vy
            self.x += self.vx
        else:
            self.vy = -self.vy
            self.y = 499 - self.r
        if self.y >= 0 + self.r:
            self.y -= self.vy
            self.x += self.vx
        else:
            self.vy = -self.vy
            self.y = 1 + self.r

        if self.x > 780 - self.r:
            self.vx = - self.vx
            self.x = 779 - self.r
        if self.x < 0 + self.r:
            self.vx = - self.vx
            self.x = 1 + self.r

        if self.live <= 0:
            canv.delete(self.id)
        else:
            self.set_coords()

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points
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


def new_game(N, event=''):
    global gun, t1, screen1, balls, bullet, score
    for i in range(N):
        t1[i + 1] = target()
        t1[i + 1].new_target()
    bullet = 0
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    canv.bind('<Motion>', g1.targetting)
    canv.bind('<Motion>', g1.targetting)
    root.bind('<KeyPress>', on_key_press)
    root.bind('<KeyRelease>', on_key_release)

    z = 0.03
    l = 0
    t1[0].live = 1
    while t1[0].live or balls:
        for b in balls:
            b.move()
            for i in range(N):
                if b.hittest(t1[i + 1]):
                    t1[i + 1].live = 0
                    t1[i + 1].hit()
                    l += 1
            if l == N:
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen1, text='Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
                t1[0].live = 0
        score = 0
        for i in range(N):
            t1[i + 1].move()
            score += t1[i + 1].points
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
