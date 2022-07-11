import random
import json

def int_input(prompt):
    while True:
        # спросить число
        number = input(prompt)
        try:
            number = int(number)
            # выйти
            if number <= 0:
                return 0
            else:
                return number
        except ValueError:
            continue

def str_input(prompt):
    return input(prompt)

def get_random_index():
    '''
    :return: список произвольных 4 индексов ,обнуляемых ячеек строки карточки
    '''
    lst = [i for i in range(9)]
    random.shuffle(lst)
    # выкидываем 5 индексов оставляемых ячеек,
    # чтобы вернуть 4 индекса обнуляемых ячеек
    for i in range(5):
        lst.pop()

    return lst

def print_cell(x):
    if x==0:
        # если ноль то пробелы
        ret = ' . '
    elif x < 0:
        # если число отрицательное (его зачеркнули) прочерк
        ret = ' * '
    elif x<10:
        # если однозначное число то пробел спереди и сзади
        ret = ' '+str(x)+' '
    else:
        # двузначные числа  пробел сзади
        ret = str(x)+' '
    return ret

def input_players(numbers_of_players):
    lst = []
    while numbers_of_players:
        player = input('Введите имя игрока (до 20 символов) и, если это компьютер, через запятую  любой символ ')
        name = player
        itiscomp = 0
        if ',' in player:
            name, itiscomp = player.split(',')
            itiscomp = 1 if itiscomp else 0
        lst.append([name,itiscomp])
        numbers_of_players -= 1
    return lst

def create_file_players(file_players):
    # спросить число игроков , если 0 - закончить программу
    numbers_of_players = int_input("Введите число игроков (0 - не играть): ")
    if not numbers_of_players:
        exit()

    lst = input_players(numbers_of_players)
    with open(file_players, 'w') as f:
        json.dump(lst, f)

