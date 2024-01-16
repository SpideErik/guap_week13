from random import randint
from tkinter import *

buttons = []
field = []


def update_button(x, y):
    if field[x][y] == 'X':
        buttons[x][y].config(bg='red')
    else:
        buttons[x][y].config(bg='green')
    buttons[x][y].config(activebackground='white')
    buttons[x][y].config(text=str(field[x][y]))


def alt_button(x, y):
    if buttons[x][y].cget('text') == 'X':
        buttons[x][y].config(text='', bg='gray', activebackground='white')
    else:
        buttons[x][y].config(text='X', bg='yellow', activebackground='white')


def print_field():
    for y in range(len(field[0])):
        for x in range(len(field)):
            print(field[x][y], end='')
        print()


def calc_x(x, y):
    global field
    w = len(field) - 1
    h = len(field[0]) - 1
    cnt = 0
    if x > 0 and y > 0 and field[x - 1][y - 1] == 'X':
        cnt += 1
    if y > 0 and field[x][y - 1] == 'X':
        cnt += 1
    if x < w and y > 0 and field[x + 1][y - 1] == 'X':
        cnt += 1
    if x > 0 and field[x - 1][y] == 'X':
        cnt += 1
    if x < w and field[x + 1][y] == 'X':
        cnt += 1
    if x > 0 and y < h and field[x - 1][y + 1] == 'X':
        cnt += 1
    if y < w and field[x][y + 1] == 'X':
        cnt += 1
    if x < w and y < h and field[x + 1][y + 1] == 'X':
        cnt += 1

    return cnt if cnt > 0 else '-'


def make_field(width, height, mines):
    """
    :param width: ширина поля
    :param height: высота поля
    :param mines: количество мин
    :return: None

    Создаем новое поле для игры и очищаем все кнопки
    """
    global buttons
    global field

    field = []

    for _ in range(width):
        field.append([0] * height)
    for _ in range(mines):
        x = randint(0, width - 1)
        y = randint(0, height - 1)
        field[x][y] = 'X'
    for y in range(width):
        for x in range(height):
            buttons[x][y].config(text='', bg='gray', activebackground='white')
            if field[x][y] != 'X':
                field[x][y] = calc_x(x, y)
    print('Обработанная карта')
    print_field()


def start_game(width, height, mines):
    """
    :param width: ширина поля
    :param height: высота поля
    :param mines: количество мин
    :return: None

    Первый запуск игры создаются кнопки и поле
    """
    global buttons
    global field

    buttons = []

    for _ in range(width):
        buttons.append([None] * height)

    for y in range(height):
        row = Frame()
        row.pack(expand=YES, fill=BOTH)
        for x in range(width):
            b = Button(row, width=4, height=2)
            buttons[x][y] = b
            b.config(command=lambda xx=x, yy=y: update_button(xx, yy))
            b.bind('<Button-3>', lambda e, xx=x, yy=y: alt_button(xx, yy))
            b.pack(expand=YES, fill=BOTH, side=LEFT)

    make_field(width, height, mines)


def new_game():
    """
    Первое нажатие на кнопку start, создавать кнопки надо только один раз
    """
    global start_button
    start_button.config(command=restart_game, text='Restart game')
    start_game(10, 10, 10)


def restart_game():
    """
    Повторное нажатие на кнопку start, надо только очистить поле и кнопки
    """
    make_field(10, 10, 10)


root = Tk()
root.title('Minesweeper')
start_button = Button(text='Start game', font='Arial 24', command=new_game)
start_button.pack()

root.mainloop()
