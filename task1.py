from random import randint
from tkinter import *
from tkinter.messagebox import showinfo

'''
Все списки двумерные для удобства обращение как [x][y]
buttons - список виджетов
field - исходное поле
pressed - нажатые кнопки
'''

buttons = []
field = []
pressed = []

'''
флаг окончания игры
'''
game_over = False


'''
сколько мин в текущей игре
'''
mines_count = 0

'''
сколько не нажатых кнопок осталось в текущей игре
'''
button_leave = 0


def update_button(x, y):
    """
    обработка нажатия кнопки
    :param open_empty: вызвать open_all_empty при нажатии на пустое место
    :param x: x
    :param y: y
    :return: None
    """
    global game_over
    global button_leave

    if pressed[x][y]:
        return
    if game_over:
        restart_game()
        return
    pressed[x][y] = True
    if field[x][y] == 'X':
        clr = 'red'
        game_over = True
    else:
        clr = 'green'
        button_leave -= 1
    buttons[x][y].config(bg =clr, activebackground=clr, relief=SUNKEN)
    buttons[x][y].config(text=str(field[x][y]))
    if button_leave == mines_count:
        showinfo('You win', 'Вы выиграли')
        game_over = True
    if not game_over and field[x][y] == '-':
        open_empty(x, y)


def alt_button(x, y):
    """
    обработка правой клавиши
    :param x: x
    :param y: y
    :return: None
    """
    if pressed[x][y]:
        return
    if buttons[x][y].cget('text') == 'X':
        buttons[x][y].config(text='', bg='gray', activebackground='white')
    else:
        buttons[x][y].config(text='X', bg='yellow', activebackground='white')


def open_empty(x, y):
    """
    если нажали на пустое поле открываем все соседние клетки
    """
    w = len(field) - 1
    h = len(field[0]) - 1
    if x > 0 and y > 0 and not pressed[x - 1][y - 1]:
        update_button(x - 1, y - 1)
    if y > 0 and not pressed[x][y - 1]:
        update_button(x, y - 1)
    if x < w and y > 0 and not pressed[x + 1][y - 1]:
        update_button(x + 1, y - 1)
    if x > 0 and not pressed[x - 1][y]:
        update_button(x-1, y)
    if x < w and not pressed[x + 1][y]:
        update_button(x+1, y)
    if x > 0 and y < h and not pressed[x - 1][y + 1]:
        update_button(x-1, y+1)
    if y < w and not pressed[x][y + 1]:
        update_button(x, y+1)
    if x < w and y < h and not pressed[x + 1][y + 1]:
        update_button(x+1, y+1)


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
    global pressed
    global mines_count
    global button_leave

    field = []
    pressed = []
    mines_count = mines
    button_leave = width*height

    for _ in range(width):
        field.append([0] * height)
        pressed.append([False]*height)
    for _ in range(mines):
        x = randint(0, width - 1)
        y = randint(0, height - 1)
        while field[x][y] == 'X':
            x = randint(0, width - 1)
            y = randint(0, height - 1)
        field[x][y] = 'X'
    for y in range(width):
        for x in range(height):
            buttons[x][y].config(text='', bg='gray', activebackground='white', relief=RAISED)
            if field[x][y] != 'X':
                field[x][y] = calc_x(x, y)
    # print('Обработанная карта')
    # print_field()


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
    global game_over
    game_over = False
    make_field(10, 10, 10)


root = Tk()
root.title('Minesweeper')
start_button = Button(text='Start game', font='Arial 24', command=new_game)
start_button.pack()

root.mainloop()
