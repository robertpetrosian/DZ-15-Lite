import classes
import functions
import os
import json

file_players='file_players.json'  # файл с игроками
yesno = 1 if os.path.exists(file_players) else 0
if yesno:
    # если файл с игроками существует , спрашиваем использовать или создать новый
    yesno = input('Файл игроков существует. Enter - ввести заново, любой символ - использовать тот же ')

if not yesno:
    # если файл с игроками не существует или хотим переписать
    functions.create_file_players(file_players)

with open(file_players) as f:
    # загружаем список игроков
    players=json.load(f)

game = classes.Game(players)  # создаем игру и передаем список игроков

while not game.over:
    barrel = game.bag.get_random_barrel()
    for i in range(len(game.players)):
        game.check_over()
        if game.over:
            break

        if game.players[i].status != -1:
            print(game.players[i])
            print(f'Выпал бочонок {barrel}')
            choice = 0
            if game.players[i].itiscomp:
                # это компьютер если есть число надо зачеркнуть, нет так нет
                choice = 1 if game.players[i].card.find_cell(barrel) != (-1, -1) else 0
            else:
                # это человек делает выбор
                otvet = functions.str_input('Выберите действие: продолжить Enter, зачеркнуть - любой символ : ')
                choice = 1 if otvet else 0

            print(f'{classes.ITISCOMP[game.players[i].itiscomp]} {game.players[i].name} ' +
                  f'выбрал действие {"зачеркнуть" if choice else "продолжить"}')
            game.players[i].check_step(barrel, choice)

print(game)


