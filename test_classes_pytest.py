import classes


class TestBag:
    def setup(self):
        self.bag = classes.Bag()

    def teardown(self):
        del self.bag

    def test_init(self):
        assert isinstance(self.bag, classes.Bag)  # это мешок
        assert isinstance(self.bag.barrels, list)  # бочонки это список
        assert self.bag.get_count_barrels() == 90  # 90 бочонков
        assert self.bag.barrels[0] == 1  # номер самого малеького
        assert self.bag.barrels[-1] == 90  # номер самого большого

    def test_get_random_barrel(self):
        barrel = self.bag.get_random_barrel()  # вытащили один случайный
        assert self.bag.get_count_barrels() == 89  # осталось 89
        assert barrel not in self.bag.barrels  # этого бочонка уже нет в мешке

        for i in range(88):  # вытащим 88 штук
            self.bag.get_random_barrel()

        assert self.bag.get_random_barrel() != 0  # вытащим последний
        assert self.bag.get_random_barrel() == 0  # возврат бочонок с номером 0 - бочонков больше нет
        assert self.bag.get_count_barrels() == 0  # в мешке пусто


class TestCard:
    """
    тестирование класса карточки
    """
    def setup(self):
        self.card = classes.Card()

    def teardown(self):
        del self.card

    def test_fill(self):
        """
        проверка заполнения карточки произвольными уникальными числами
        :return:
        """
        self.card.fill()
        assert self.card.card[0] != self.card.card[1] != self.card.card[2] , \
            "какие-то линии карточки одинаковы :\n"+\
            f"1-я {self.card.card[0]} \n"+\
            f"2-я {self.card.card[1]} \n"+ \
            f"3-я {self.card.card[2]} \n"

        assert len(set(self.card.card[0] + self.card.card[1] + self.card.card[2])) == 27 ,\
            "не все ячейки уникальны"

        for row in range(3):
            #  проверка в ячейке или 0, или 90, или её колонка равна кол-ву десятков
            for col in range(9):
                cell = self.card.card[row][col]
                assert cell == 0 or \
                       cell//10 == self.card.card[row].index(cell) or \
                       cell==90, f"неверное число {cell} в {row}, {col}"

    def test_zero_random4(self):
        self.card.fill()
        self.card.zero_random4()
        print((self.card.card))
        assert self.card.card[0].count(0) == 4, "не 4 ячейки 1й линии пустые"
        assert self.card.card[1].count(0) == 4, "не 4 ячейки 2й линии пустые"
        assert self.card.card[2].count(0) == 4, "не 4 ячейки 3й линии пустые"

        self.card = classes.Card()

    def test_init(self):
        self.card = classes.Card()
        assert isinstance(self.card, classes.Card) , "не создан экземпляр класса "
        assert isinstance(self.card.card, list)  , " содержание карточки не есть список"
        assert len(self.card.card) == 3 , " у карточки не три линии "

        # каждая линия список и состоит из 9 ячеек и 4 ячейки пустые
        assert isinstance(self.card.card[0], list) , "первая линия это не список"
        assert len(self.card.card[0]) == 9 , "количество ячеек в1й линии не 9"
        assert self.card.card[0].count(0) == 4, "не 4 ячейки 1й линии пустые"
        assert isinstance(self.card.card[1], list), "2я линия это не список"
        assert len(self.card.card[1]) == 9 , "количество ячеек в 2й линии не 9"
        assert self.card.card[1].count(0) == 4, "не 4 ячейки 2й линии пустые"
        assert isinstance(self.card.card[2], list), "3я линия это не список"
        assert len(self.card.card[2]) == 9  , "количество ячеек в 1й линии не 9"
        assert self.card.card[2].count(0) == 4, "не 4 ячейки 3й линии пустые"

        for row in range(3):
            #  проверка в ячейке или 0, или 90, или её колонка равна кол-ву десятков
            for col in range(9):
                cell = self.card.card[row][col]
                assert cell == 0 or \
                       cell//10 == self.card.card[row].index(cell) or \
                       cell == 90, f"неверное число {cell} в {row}, {col}"

        # проверка зачеркивания
        for number in range(1, 91):
            # проходим по ряду
            if self.card.find_cell(number):
                row, col = self.card.find_cell(number)  # находим ячейку с таким числом
                assert self.card.card[row][col] == number  # ячейка должна быть числом
                assert self.card.cross_cell(number)  # изменение знака произошло успешно
                assert self.card.card[row][col] == -1 * number  # ячейка должна числом со знаком "-"

        # теперь карточка "пустая" - нули или все зачеркнуты
        assert self.card.card_empty()

        # проверка начального заполнения карточки и вычеркивания 4 случайных ячеек

    def test_print_card(self):
        self.card.card = [[1,0,3,-10,5,0,7,0,9],
                          [1,2,3,-4,5,6,7,8,9],
                          [1,2,3,4,0,60,7,8,9]]
        assert str(self.card) == ' 1  .  3  *  5  .  7  .  9 \n'+' 1  2  3  *  5  6  7  8  9 \n'+' 1  2  3  4  . 60  7  8  9 \n'
        self.setup()

    def test_cross_cell(self):
        self.card.card = [[1,0,3,-10,5,0,7,0,9],
                          [1,2,3,-4,5,6,7,8,9],
                          [1,2,3,4,0,60,7,8,9]]
        assert self.card.cross_cell(60) , "число 60 не (найдено и зачеркнуто)"
        assert self.card.card[2][5] == -60 , "число не изменено на противоположное"

        self.setup()
    def test_find_cell(self):
        self.card.card = [[1,0,3,-10,5,0,7,0,9],
                          [1,2,3,-4,5,6,7,8,9],
                          [1,2,3,4,0,60,7,8,9]]
        assert self.card.find_cell(7) == (0,6)
        assert self.card.find_cell(0) == (0,1)
        assert self.card.find_cell(17) == 0
        assert self.card.find_cell(60) == (2,5)
        assert self.card.find_cell(-4) == (1,3)

        self.setup()
class TestPlayer:
    def setup(self):

        self.pl = classes.Player('komp',1)

    def teardown(self):
        del self.pl

    def test_init(self):
        assert self.pl.name == 'komp'
        assert self.pl.itiscomp == 1
        assert isinstance(self.pl.card, classes.Card)
        assert self.pl.status == 0

class TestGame:
    """
    тестирование игры
    """
    def setup(self):
        players = []
        players.append(['John',0])
        players.append(['Jannet', 0])
        players.append(['Riva', 1])
        self.players = players
        self.game = classes.Game(players)

    def teardown(self):
        del self.players

    def test_check_over(self):
        """
        тестирование игра закончена при одном из условий
        - мешок пустой
        - есть один победитель
        - нет играющих
        """

        self.setup()
        self.game.check_over()
        assert self.game.over == 0, "у всех игроков статус играет, а игра завершена"

        self.setup()
        self.game.bag.barrels.clear() # опустошить мешок
        self.game.check_over()
        assert self.game.over == 1 , "мешок пуст , а игра продолжается"

        self.setup()
        self.game.players[0].status = -1
        self.game.check_over()
        assert  self.game.over == 0, "только один проигравший и игра завершена"

        self.setup()
        self.game.players[0].status = 1
        self.game.check_over()
        assert self.game.over == 1, "только один выигравший и игра не завершена"

        self.setup()
        self.game.players[0].status = 1
        self.game.players[1].status = 1
        self.game.players[2].status = 1
        self.game.check_over()
        assert self.game.over == 1, "все выиграли и игра не завершена"

        self.setup()
        self.game.players[0].status = -1
        self.game.players[1].status = -1
        self.game.players[2].status = -1
        self.game.check_over()
        assert self.game.over == 1, "все проиграли и игра не завершена"

    def test_print_over(self):
        self.setup()
        self.game.players[0].status = 1
        self.game.players[1].status = -1
        self.game.players[2].status = 0

        resultat = str(self.game)
        text = 'Игра продолжается.\n'+\
        'Победители:\n'+ classes.ITISCOMP[self.game.players[0].itiscomp] + ' ' + self.game.players[0].name + '\n'+\
        'Играющие:\n'  + classes.ITISCOMP[self.game.players[2].itiscomp] + ' ' + self.game.players[2].name + '\n'+\
        'Проигравшие:\n'+classes.ITISCOMP[self.game.players[1].itiscomp] + ' ' + self.game.players[1].name + '\n'

        assert resultat == text

