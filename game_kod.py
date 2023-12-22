from tkinter import *
import random

GRID_SIZE = 20  
SQUARE_SIZE = 20  
MINES_NUM = 40   
mines = set(random.sample(range(1, GRID_SIZE**2+1), MINES_NUM))  #распределение мин по полю
clicked = set()  #уже открытые клетки


def check_mines(neighbors):  #функция возвращает количество мин вокруг neighbors
    return len(mines.intersection(neighbors))


def generate_neighbors(square):  #возвращает соседние клетки с square
    if square == 1:                                         #левая верхняя клетка
        data = {GRID_SIZE + 1, 2, GRID_SIZE + 2}
    elif square == GRID_SIZE ** 2:                          #правая нижняя
        data = {square - GRID_SIZE, square - 1, square - GRID_SIZE - 1}
    elif square == GRID_SIZE:                               #левая нижняя
        data = {GRID_SIZE - 1, GRID_SIZE * 2, GRID_SIZE * 2 - 1}
    elif square == GRID_SIZE ** 2 - GRID_SIZE + 1:          #верхняя правая
        data = {square + 1, square - GRID_SIZE, square - GRID_SIZE + 1}
    elif square < GRID_SIZE:                                #клетка в левом ряду
        data = {square + 1, square - 1, square + GRID_SIZE,
                square + GRID_SIZE - 1, square + GRID_SIZE + 1}
    elif square > GRID_SIZE ** 2 - GRID_SIZE:               #клетка в правом ряду
        data = {square + 1, square - 1, square - GRID_SIZE,
                square - GRID_SIZE - 1, square - GRID_SIZE + 1}
    elif square % GRID_SIZE == 0:                           #клетка в нижнем ряду
        data = {square + GRID_SIZE, square - GRID_SIZE, square - 1,
                square + GRID_SIZE - 1, square - GRID_SIZE - 1}
    elif square % GRID_SIZE == 1:                           #клетка в верхнем ряду
        data = {square + GRID_SIZE, square - GRID_SIZE, square + 1,
                square + GRID_SIZE + 1, square - GRID_SIZE + 1}
    else:                                                   # Любая другая клетка
        data = {square - 1, square + 1, square - GRID_SIZE, square + GRID_SIZE,
                square - GRID_SIZE - 1, square - GRID_SIZE + 1,
                square + GRID_SIZE + 1, square + GRID_SIZE - 1}
    return data


def clearance(ids):   #функция очистки поля
    clicked.add(ids) 
    ids_neigh = generate_neighbors(ids) 
    around = check_mines(ids_neigh) 
    c.itemconfig(ids, fill="green") 

    if around == 0:                         #если вокруг мин нет
        neigh_list = list(ids_neigh)
        while len(neigh_list) > 0:
            item = neigh_list.pop()
            c.itemconfig(item, fill="green")
            item_neigh = generate_neighbors(item)
            item_around = check_mines(item_neigh)
            if item_around > 0:
                #проверка
                if item not in clicked:
                    x1, y1, x2, y2 = c.coords(item)
                    c.create_text(x1 + SQUARE_SIZE / 2,
                                  y1 + SQUARE_SIZE / 2,
                                  text=str(item_around),
                                  font="Arial {}".format(int(SQUARE_SIZE / 2)),
                                  fill='yellow')
            else:    #если в соседних клетках мин нет
                neigh_list.extend(set(item_neigh).difference(clicked))
                neigh_list = list(set(neigh_list))
            clicked.add(item)
    else:                                   #если мины вокруг есть
        x1, y1, x2, y2 = c.coords(ids)
        c.create_text(x1 + SQUARE_SIZE / 2,
                      y1 + SQUARE_SIZE / 2,
                      text=str(around),
                      font="Arial {}".format(int(SQUARE_SIZE / 2)),
                      fill='yellow')



def click(event):   #функция нажатия на клетку
    ids = c.find_withtag(CURRENT)[0]
    if ids in mines:
        c.itemconfig(CURRENT, fill="red")
        lose()
    elif ids not in clicked:
        clearance(ids)
        c.itemconfig(CURRENT, fill="green")
    c.update()


flags = set()
def mark_mine(event):  #функция довавления флага на преполагаемую мину
    ids = c.find_withtag(CURRENT)[0]
    if ids not in clicked:
        if ids not in flags:    #если клетка еще не отмечена флагом добавляем флаг
            x1, y1, x2, y2 = c.coords(ids)
            c.create_text(x1 + SQUARE_SIZE / 2, y1 + SQUARE_SIZE / 2, text='F',
                          font="Arial {}".format(int(SQUARE_SIZE / 2)), fill='black')
            flags.add(ids)
        else:                   #убираем флаг   
            c.itemconfig(CURRENT, fill="gray")
            c.delete(c.find_withtag(CURRENT)[1])
            flags.remove(ids)
    check_win()


def lose():        #функция проигрыша
    loseWindow = Tk()
    loseWindow.title('Вы проиграли:(')
    loseWindow.geometry('300x100')
    loseLabe = Label(loseWindow, text = 'В следующий раз повезет больше!')
    loseLabe.pack()
    loseWindow.mainloop()


def check_win():   #функция проверки победы
    if flags == mines:
        win()

def win():         #функция победы
    winWindow = Tk()
    winWindow.title('Вы выиграли!')
    winWindow.geometry('300x100')
    winLabel = Label(winWindow, text = 'Поздравляем! Вы обезвредили все мины!')
    winLabel.pack()
    winWindow.mainloop()



root = Tk()
root.title("сапер")
c = Canvas(root, width=GRID_SIZE * SQUARE_SIZE, height=GRID_SIZE * SQUARE_SIZE)
c.bind("<Button-1>", click)       #нажатие левой кнопки мыши
c.bind("<Button-3>", mark_mine)   #нажатие правой кнопки мыши (если у вас macOS нужно изменить на Button-2)
c.pack()
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
      c.create_rectangle(i * SQUARE_SIZE, j * SQUARE_SIZE,
                         i * SQUARE_SIZE + SQUARE_SIZE,
                         j * SQUARE_SIZE + SQUARE_SIZE, fill='gray')
root.mainloop()