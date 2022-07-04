import classes

def test_bag():
    bag = classes.Bag() # создали полный мешок
    assert isinstance(bag,(classes.Bag)) # это мешок
    assert isinstance(bag.barrels, (list)) # бочонки это список
    assert bag.get_count_barrels() == 90 # 90 бочонков
    assert bag.barrels[0] == 1 # номер самого малеького
    assert bag.barrels[-1] == 90 # номер самого большого
    barrel = bag.get_random_barrel() # вытащили один случайный
    assert bag.get_count_barrels() == 89 # осталось 89
    assert barrel not in bag.barrels # этого бочонка уже нет в мешке
    for i in range(88): # вытащим 88 штук
        barrel = bag.get_random_barrel()
    assert bag.get_random_barrel() != 0 # вытащим последний
    barrel = bag.get_random_barrel() # попытаемся ватщить еще
    assert bag.get_random_barrel() == 0 # возврат бочонок с номером 0 - бочонков больше нет
    assert bag.get_count_barrels() == 0 # в мешке пусто

def test_card():
    card = classes.Card() # создать экземпляр
    assert isinstance(card,(classes.Card)) # принадлежит классу
    assert isinstance(card.card, (list)) # карточка есть список
    assert len(card.card) == 3 # три линии карточки
    assert isinstance(card.card[0], (list)) # 1-я линия список
    assert len(card.card[0]) == 9 # 9 ячеек 1й линии
    assert isinstance(card.card[1], (list)) #
    assert len(card.card[1]) == 9 #
    assert isinstance(card.card[2], (list)) #
    assert len(card.card[2]) == 9 #
    assert card.card[0].count(0) == 4 # 4 ячейки 1й линии пустые
    assert card.card[1].count(0) == 4 #
    assert card.card[2].count(0) == 4 #
    for row in range(3):
        #  проверка в ячейке или 0, или 90, или её колонка равна кол-ву десятков
        for col in range(9):
            cell = card.card[row][col]
            assert cell == 0 or cell//10 == card.card[row].index(cell) or cell==90

    # проверка зачеркивания
    for number in range(1,91):
        # проходим по ряду
        (row,col) = card.find_cell(number)         # находим ячейку с таким числом
        if row == -1 and col == -1:               # если ячейка с таким числом не найдена - пропуск
            pass
        else:
            assert card.card[row][col] == number  # ячейка должна быть числом
            assert card.cross_cell(number) # изменение знака произошло успешно
            assert card.card[row][col] == -1 * number # ячейка должна числом со знаком "-"

    # теперь карточка "пустая" - нули или все зачеркнуты
    assert card.card_empty()

def test_player():
    pl = classes.Player(1,'komp')
    assert pl.name == 'komp' #
    assert pl.itiscomp == 1 #
    assert isinstance(pl.card, (classes.Card)) #
    assert pl.status == 0 #

