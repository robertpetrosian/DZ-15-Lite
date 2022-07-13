import random
import functions
STATUS = {-1: 'проиграл',
          1: "выиграл",
          0: "играет"}

ITISCOMP = {0: 'человек',
            1: 'компьютер'}


class Game:
    """
    класс игра
    """
    def __init__(self, players):

        # список играющих . их статус: 0 играет 1 выиграл -1 проиграл
        # проигравшие выводятся из списка, чтобы не участвовали в дальнейших шагах

        self.bag = Bag()  # мешок с бочонками
        self.over = 0  # игра завершена , если равно 1
        self.players = []
        for item in players:
            # создание играющих
            name = item[0]
            itiscomp = item[1]
            self.players.append(Player(name,itiscomp))

    def check_over(self):
        """
        # проверка мешка и игроков на то, что игра окончена
        :return: True or False
        """
        # считаем игроков
        kol_win = 0   # победители
        kol_los = 0   # проигравшие
        kol_play = 0  # играющие

        for i in range(len(self.players)):
            if self.players[i].status == 1:
                kol_win += 1
            elif self.players[i].status == -1:
                kol_los += 1
            elif self.players[i].status == 0:
                kol_play += 1

        if kol_play == 0 and kol_win == 0:
            #  играющих и победителей нет все проиграли
            self.over = 1
        elif not self.bag.get_count_barrels():
            # игра завершена если в мешке нет бочонков , проиграли все
            self.over = 1
            for i in range(len(self.players)):
                self.players[i].status = -1
        elif kol_win >= 1:
            # есть победители, игра завершена , играющие становятся програвщими
            self.over = 1
            for i in range(len(self.players)):
                if self.players[i].status == 0:
                    self.players[i].status = -1
        elif kol_play == 1:
            # остался один игрок , игра завершена, он победил
            self.over = 1
            for i in range(len(self.players)):
                if self.players[i].status == 0:
                    self.players[i].status = 1
                    break

        for i in range(len(self.players)):
            # ищем хотя бы одного выигравшего
            if self.players[i].status == 1:
                self.over = 1

        count = 0
        for i in range(len(self.players)):
            #     количество играющих игроков = 1
            if self.players[i].status == 0:
                count += 1
        if count == 1:
            self.over = 1

        if self.over == 1:
            # если игра завершена, все игроки со статусом 0 получают статус проигравших
            for i in range(len(self.players)):
                if self.players[i].status == 0:
                    self.players[i].status = -1

    def __str__(self):
        # вывод строки для печати результата игры
        resultat = 'Игра завершена.\n' if self.over else 'Игра продолжается.\n'
        resultat += 'Победители:\n'
        for i in range(len(self.players)):
            if self.players[i].status == 1:
                resultat += ITISCOMP[self.players[i].itiscomp]+' '+ self.players[i].name+ '\n'

        resultat += 'Играющие:\n'
        for i in range(len(self.players)):
            if self.players[i].status == 0:
                resultat += ITISCOMP[self.players[i].itiscomp]+' '+ self.players[i].name+ '\n'

        resultat += 'Проигравшие:\n'
        for i in range(len(self.players)):
            if self.players[i].status == -1:
                resultat += ITISCOMP[self.players[i].itiscomp]+' '+ self.players[i].name + '\n'

        return resultat

class Bag:
    """
    мешок
    м заполнить
    м вытащить бочонок
        перемешать
        вытащить pop() IndexError
    """

    def __init__(self):
        """
        инициализация = заполнить мешок бочонками
        """
        self.barrels = self.fill_bag()

    def fill_bag(self):
        """
        получить мешок из 90 бочонков
        :return: список из 90 бочонков
        """
        self.barrels = [i for i in range(1, 91)]
        return self.barrels

    def get_random_barrel(self) -> int:
        """
        перемешать мешок и вытащить произвольный бочонок
        :return:
        """
        random.shuffle(self.barrels)
        try:
            ret = self.barrels.pop()
        except IndexError:
            # мешок пуст
            ret = 0
        return ret

    def get_count_barrels(self):
        """
        проверка пустой мешок или нет
        :return: количество оставшихся бочонков
        """
        return len(self.barrels)


class Card:
    """
    карточка - 2-мерный список integer (3,9).
                числа не повторяются,
                в каждой линии 5 чисел , сортировка по возрастанию

                Замечание.вообще-то говоря, в настоящем лото карточка строится по-другому
                и приведенные примеры нерелевантны
                9 колонок означают 9 десятков чисел. и одно число лежит в соответствующей колонке
                есть исключение первая колонка от 1 по 9 (9 чисел)
                последняя колонка от 80 по 90 (11 чисел)

                Рассмотрим пример. числа 2 и 9 должны быть в одной колонке
                во второй строчке числа 75 и 78 не могут быть на одной строчке
                почти все числа стоят не в своих колонках
                --------------------------
                    9 43 62          74 90
                 2    27    75 78    82
                   41 56 63     76      86
                --------------------------

                К чему это я?
                К тому, что появляется вопрос "где ставить пробелы между числами?"
                Если принимать правила в ТЗ , то ставить надо хаотично и помнить эти пробелы и
                    фактически придумывать свои правила

                С другой стороны, сделать игру по настоящим правилам сложнее и интереснее
                Поэтому пойду этим путём
    """
    def __init__(self):
        """
        создать карточку
        """
        self.fill()
        self.zero_random4()

    def fill(self):
        """
        алгоритм заполнения карточки:
            берем мешок с бочонками
            вытаскиваем произвольный бочонок
            заполняем всю (3*9) карточку согласно принципу колонка ~ десятка ,
                                не забывая про особенности первой и последней
                если например уже выпало три бочонка из 70-79 и выпадает 4й ставим сверху (заменяем)
                пока не останется пустых ячеек

            в каждой линии карточки  обнуляем 4 ячейки по произвольному индексу с 0 по 8

        :return: заполненная карточка
        """

        bag = Bag()  # наполнить мешок
        line = [0 for i in range(9)]
        card = [line.copy() , line.copy(), line.copy()]

        while card[0].count(0) + card[1].count(0) + card[2].count(0):
            # делать пока есть хотя бы один 0 в строке
            bochka = bag.get_random_barrel()       # взять бочонок
            col = bochka // 10 if bochka < 90 else 8    # расчет колонки, 90 ставится в посл колонку

            # смотрим в 1й или 2й  линии свободное место ,
            # если нет то вставляем в 3ю линию
            if card[0][col] == 0:
                card[0][col] = bochka
            elif card[1][col] == 0:
                card[1][col] = bochka
            elif card[2][col] == 0:
                card[2][col] = bochka
        self.card=card.copy()

    def zero_random4(self):
        # пройти по строкам карточки и обнулить по 4 произвольных ячейки
        for row in [0, 1, 2]:
            for i in functions.get_random_index():
                self.card[row][i] = 0

    def __str__(self):
        """
        :return: строка состоящую из 3 линий ячеек в строковм виде,
        """
        ret = ''
        for row in range(3):
            # проход по строкам
            for col in range(9):
                # проход по колонкам
                ret += functions.print_cell(self.card[row][col])
            ret += '\n'
        return ret

    def cross_cell(self, number):
        if self.find_cell(number):
            # число найдено
            # делаю число отрицательным чтобы сохранить значение (для отладки),
            # печататься будет *
            row, col = self.find_cell(number)
            self.card[row][col] *= -1
            return True
        else:
            return False


    def find_cell(self, number):
        """
        найти число в карточке
        :param number: число, которое ищем
        :return: кортеж (строка, колонка) или 0 если неуспех
        """
        for row in range(3):
            # проход по строкам
            for col in range(9):
                # проход по колонкам
                if self.card[row][col] == number:
                    return row, col
        return 0

    def card_empty(self):
        """
        проверяет есть ли ячейки > 0
        :return: True если нет таких ячеек, False наоборот
        """
        for row in range(3):
            for col in range(9):
                if self.card[row][col] > 0:
                    return False
        return True


class Player:
    """
    игрок
        с это компьютер itiscomp
        с имя name
        с статус status
        с карточка card
        м создать
            спросить имя (не пустое, длина=20)
            карточка создать
            присвоить статус "играет"
            присвоить тип игрока
        м присвоить статус
    """
    count_players = 0

    def __init__(self, name , itiscomp):
        self.name = name
        self.itiscomp= itiscomp
        self.card = Card()
        self._status = 0

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, number):
        number =  1 if number > 0 else number
        number = -1 if number < 0 else number
        self._status = number

    def __str__(self):
        ret = f'{ITISCOMP[self.itiscomp]} {self.name}. Статус {STATUS[self.status]}. Карта: \n'
        ret += str(self.card)
        return ret

    def check_step(self, barrel, step):
        # проверка верно или нет сделан ход и
        # установка статуса проиграл если ошибся
        # установка статуса выиграл если зачеркнул последнее число на карточке
        if step:  # реакция : надо зачеркнуть
            checked = 1 if self.card.find_cell(barrel) else 0  # проверку не  прошел / прошел#
        else:  # реакция : не надо зачеркнуть
            checked = 0 if self.card.find_cell(barrel)  else 1  # проверку  прошел# /  не прошел

        if checked:
            if self.card.find_cell(barrel) :
                self.card.cross_cell(barrel)
                if self.card.card_empty():
                    self.status = 1
        else:  # проверку не прошел - проиграл
            self.status = -1
