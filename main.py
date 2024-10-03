from tkinter import *
from tkinter import font, messagebox
import random

GRID_SIZE = 10 # Размер игрового поля

# Создаем двумерные массивы для инициализации полей игрока и врага, где 0 - пустая клетка
player_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
ai_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1] # Виды и кол-во кораблей

def place_ship_randomly(grid: list, ship_size: int):
    """Функция рандомной расстановки кораблей"""
    placed = False
    while not placed: # Предотвращение потери кораблей в случае неудачного расположения с первого раза
        orientation = random.choice(['horizontal', 'vertical']) # Случайный выбор ориентации корабля
        match orientation:
            case 'horizontal':
                row = random.randint(0, GRID_SIZE - 1)
                column = random.randint(0, GRID_SIZE - ship_size)
                if all(grid[row][column + i] == 0 for i in range(ship_size)): # Проверка, что корабль влезает
                    for i in range(ship_size):
                        grid[row][column + i] = 1 # Заполнение поля кораблями
                    placed = True # Подтверждение успешного расположения корабля
            case 'vertical':
                row = random.randint(0, GRID_SIZE - ship_size)
                column = random.randint(0, GRID_SIZE - 1)
                if all(grid[row + i][column] == 0 for i in range(ship_size)):
                    for i in range(ship_size):
                        grid[row + i][column] = 1
                    placed = True

for ship in SHIP_SIZES: # Расставление кораблей для игрока и ИИ
    place_ship_randomly(player_grid, ship)
    place_ship_randomly(ai_grid, ship)
    

root = Tk()
root.title('Морской бой') # Название окна

# Настройка шрифта
custom_font = font.Font(family='Helvetica', size=14, weight='bold', slant='roman')

# Разделение нашего окна на 2 поля боя
player_frame = Frame(root, bg='brown')
ai_frame = Frame(root, bg='red')
player_frame.pack(side='left', padx=20, pady=20)
ai_frame.pack(side='right', padx=20, pady=20)

"""
# Надписи для фреймов
player_label = Label(player_frame, text='Ваше поле боя', font=custom_font)
player_label.place(x=15, y=50) # pady - ширина линии
ai_label = Label(ai_frame, text='Поле врага', font=custom_font)
ai_label.grid(row=1, column=0, columnspan=GRID_SIZE, pady=(0,10))
"""

def create_grid(frame, grid, is_player=True):
    """Создание сетки"""
    buttons = []
    for row in range(GRID_SIZE):
        button_row = []
        for column in range(GRID_SIZE):
            if is_player:
                if grid[row][column] == 1: # Для игрока отображаем корабли
                    color = 'gray'
                else:
                    color = 'blue' # Пустое поле
                btn = Label(frame, width=2, height=1, bg=color, borderwidth=1, relief='solid')
            else:
                # Для поля ИИ испольуем кнопки для стрельбы
                btn = Button(frame, width=2, height=1, bg='blue',
                             command=lambda r=row, c=column: player_fire(r,c))
            btn.grid(row=row, column = column)
            button_row.append(btn)
        buttons.append(button_row)
    return buttons

def update_player_grid():
    """Обновление ячеек"""
    for row in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            if player_grid[row][column] == 1: # Корабль
                player_buttons[row][column].config(bg='gray')
            elif player_grid[row][column] == 2: # Поражение
                player_buttons[row][column].config(bg='red')
            elif player_grid[row][column] == 3: # Промах
                player_buttons[row][column].config(bg='white')

def update_ai_grid():
    for row in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            if ai_grid[row][column] == 2:
                ai_buttons[row][column].config(bg='red', state='disabled')
            elif ai_grid[row][column] == 3:
                ai_buttons[row][column].config(bg='white', state='disabled')

# Функции для выстрелов
def player_fire(row, col):
    if ai_grid[row][col] in [2,3]:
        # Уже стреляли сюда
        return
    if ai_grid[row][col] == 0:
        ai_grid[row][col] = 3  # Промах
        ai_buttons[row][col].config(bg='white', state='disabled')
        ai_turn()
    elif ai_grid[row][col] == 1:
        ai_grid[row][col] = 2  # Попадание
        ai_buttons[row][col].config(bg='red', state='disabled')
        if check_win(ai_grid):
            messagebox.showinfo("Победа!", "Вы победили ИИ!")
            root.destroy()

ai_hits = []

def ai_turn():
    global ai_hits
    while True:
        if ai_hits:
            last_hit = ai_hits[-1]
            # Попытка стрелять вокруг последнего попадания
            potential_moves = [
                (last_hit[0]-1, last_hit[1]),
                (last_hit[0]+1, last_hit[1]),
                (last_hit[0], last_hit[1]-1),
                (last_hit[0], last_hit[1]+1)
            ]
            # Фильтрация корректных и нестреляных клеток
            potential_moves = [
                (r, c) for r, c in potential_moves
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and player_grid[r][c] not in [2,3]
            ]
            if potential_moves:
                row, col = random.choice(potential_moves)
            else:
                # Если вокруг последнего попадания уже все клетки стреляли, выбираем случайную
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - 1)
        else:
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
        
        if player_grid[row][col] in [0,1]:
            if player_grid[row][col] == 1:
                player_grid[row][col] = 2  # Попадание
                player_buttons[row][col].config(bg='red', state='disabled')
                ai_hits.append((row, col))
                if check_win(player_grid):
                    messagebox.showinfo("Поражение", "ИИ победил вас!")
                    root.destroy()
                break
            else:
                player_grid[row][col] = 3  # Промах
                player_buttons[row][col].config(bg='white')
                break

# Функция для проверки победы
def check_win(grid):
    for row in grid:
        if 1 in row:
            return False
    return True


player_buttons = create_grid(player_frame, player_grid, is_player=True)
ai_buttons = create_grid(ai_frame, ai_grid, is_player=False)

# Обновляем отображение
update_player_grid()
update_ai_grid()


if __name__ == '__main__':
    root.mainloop()
