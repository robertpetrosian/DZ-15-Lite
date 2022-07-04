import classes

while True:
    # спросить число игроков и цикл пока не ответит или 0 - закончить программу
    numbers_of_players = input("Введите число игроков (0 - не играть): ")
    try:
        numbers_of_players = int(numbers_of_players)
        # выйти из игры или цикла
        if numbers_of_players <= 0:
            exit()
        else:
            break
    except ValueError:
        continue

game = classes.Game(numbers_of_players) # кол игроков
bag = game.bag

while not game.over:
    barrel = game.bag.get_random_barrel()
    for i in range(len(game.players)):
        game.check_over()
        if game.over:
            break

        if game.players[i].status != -1:
            game.players[i].info()
            print(f'Выпал бочонок {barrel}')
            ret = 0
            if game.players[i].itiscomp:
                # это компьютер если есть число надо зачеркнуть, нет так нет
                ret = 1 if game.players[i].card.find_cell(barrel) != (-1, -1) else 0
            else:
                # это человек делает выбор
                otvet = input('Выберите действие: продолжить Enter, зачеркнуть - любой символ : ')
                ret = 1 if otvet else 0

            print(f'{classes.ITISCOMP[game.players[i].itiscomp]} {game.players[i].name} '+
                f'выбрал действие {"зачеркнуть" if ret else "продолжить"}')
            game.players[i].check_step(barrel, ret)

game.print_over()
