from tkinter import *
from tkinter import font

root = Tk()
root.withdraw() # Скрываем главное окно
player1 = Toplevel(root) # Дочернее окно для 1-го игрока
player2 = Toplevel(root) # Дочернее окно для 2-го игрока

# Создание окон для каждого игрока
player1.geometry('600x400')
player2.geometry('600x400')
player1.title('Игрок №1')
player2.title('Игрок №2')


# Разделительная черта посередине для разделения своего окна и соперника
for _ in range(19):
    Label(player1, text='|').pack()
    Label(player2, text='|').pack()
    
custom_font_1 = font.Font(family='Helvetica', size=16, weight='bold', slant='roman')

Label(player1, text='Ваше поле боя', font=custom_font_1).place(x=75, y=5)
Label(player1, text='Поле врага', font=custom_font_1).place(x=395, y=5)

custom_font_2 = font.Font(family='Helvetica', size=16, weight='bold', slant='roman')

Label(player2, text='Ваше поле боя', font=custom_font_2).place(x=75, y=5)
Label(player2, text='Поле врага', font=custom_font_2).place(x=395, y=5)




if __name__ == '__main__':
    root.mainloop()
