import random
STATUS = {-1:'проиграл',
          1:"выиграл",
          0:"играет"}

ITISCOMP = {0:'человек',
            1:'компьютер'}

class Game():
    '''
    класс игра
    '''
    def __init__(self, num_of_players):
        def create_player():
            name = input('Введите имя игрока (до 20 символов) ')
            # если не ввел имя то генерируем
            kod = str(random.randint(1,1000))
            name = 'Player'+kod if not name else name

            name = name[:20]
            itiscomp = input(f'{name} - человек ? Enter - да, любой символ нет ')
            itiscomp = 1 if itiscomp else 0

            return Player(itiscomp=itiscomp, name=name)

        self.bag = Bag() # мешок с бочонками
        self.over = 0 # игра завершена , если равно 1

        # список играющих . их статус 0 играют или 1 выиграл
        # проигравшие выводятся из списка, чтобы не участвовали в дальнейших шагах
        self.players = []
        for i in range(num_of_players):
            # создание играющих
            self.players.append(create_player())

    def check_over(self):
        '''
        # проверка мешка и игроков на то, что игра окончена
        :return: True or False
        '''

        # считаем игроков

        kol_win=0 # победители
        kol_los=0 # проигравшие
        kol_play=0 # играющие

        for i in range(len(self.players)):
            if self.players[i].status == 1:
                kol_win += 1
            elif self.players[i].status == -1:
                kol_los += 1
            elif self.players[i].status == 0:
                kol_play += 1

        if kol_play==0 and kol_win==0:
            #  играющих и победителей нет все проиграли
            self.over = 1
        elif not self.bag.get_count_barrels() :
            # игра завершена если в мешке нет бочонков , проиграли все
            self.over = 1
            for i in range(len(self.players)):
                self.players[i].status = -1
        elif kol_win >=1:
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

        count=0
        for i in range(len(self.players)):
            #     количество играющих игроков =1
            if self.players[i].status == 0:
                count += 1
        if count==1:
            self.over = 1

        if self.over == 1:
            # если игра завершена, все игроки со статусом 0 получают статус проигравших
            for i in range(len(self.players)):
                if self.players[i].status == 0:
                    self.players[i].status = -1


    def print_over(self):
        # печать результата игры
        print('Игра завершена.')
        print('Победители:')
        for i in range(len(self.players)) :
            if self.players[i].status == 1:
                print(f'{ITISCOMP[self.players[i].itiscomp]} {self.players[i].name}')
        print('Проигравшие:')
        for i in range(len(self.players)) :
            if self.players[i].status == -1:
                print(f'{ITISCOMP[self.players[i].itiscomp]} {self.players[i].name}')

class Bag():
    '''
    мешок
    м заполнить
    м вытащить бочонок
        перемешать
        вытащить pop() IndexError

    '''

    def __init__(self):
        '''
        инициализация = заполнить мешок бочонками
        '''
        self.barrels = self.fill_bag()


    def fill_bag(self):
        '''
        получить мешок из 90 бочонков
        '''
        self.barrels = [i for i in range(1,91)]
        return self.barrels

    def get_random_barrel(self):
        '''
        перемешать мешок и вытащить последний бочонок
        :return:
        '''
        random.shuffle(self.barrels)
        try:
            ret = self.barrels.pop()
        except IndexError:
            ret = 0
        return ret

    def get_count_barrels(self):
        '''
        проверка пустой мешок или нет
        :return: количество оставшихся бочонков
        '''
        return len(self.barrels)

class Card():
    '''
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
    '''
    def __init__(self):
        '''
        создать карточку
        '''
        self.card = self.fill()

    def fill(self):
        '''
        алгоритм заполнения карточки:
            берем мешок с бочонками
            вытаскиваем произвольный бочонок
            заполняем всю (3*9) карточку согласно принципу колонка ~ десятка ,
                                не забывая про особенности первой и последней
                если например уже выпало три бочонка из 70-79 и выпадает 4й ставим сверху (заменяем)
                пока не останется пустых ячеек

            в каждой линии карточки  обнуляем 4 ячейки по произвольному индексу с 0 по 8

        :return: заполненная карточка
        '''

        def get_random_index():
            '''
            :return: список произвольных 4 индексов ,обнуляемых ячеек строки карточки
            '''
            lst = [i for i in range(9)]
            random.shuffle(lst)
            # выкидываем 5 индексов оставляемых ячеек, чтобы вернуть 4 индекса обнуляемых чеек
            lst.pop()
            lst.pop()
            lst.pop()
            lst.pop()
            lst.pop()
            return lst

        bag = Bag()  # наполнить мешок
        card = [[0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0]]

        counter=0
        while card[0].count(0)+card[1].count(0)+card[2].count(0) :
            # делать пока есть хотя бы один 0 в строке
            bochka = bag.get_random_barrel()       # взять бочонок
            col = bochka // 10 if bochka < 90 else 8    # расчет колонки, 90 ставится в посл колонку

            if card[0][col] == 0:
                card[0][col] = bochka
            elif card[1][col] == 0:
                card[1][col] = bochka
            else:
                card[2][col] = bochka

        # пройти по строкам карточки и обнулить по 4 произвольных ячейки
        for row in [0,1,2]:
            for i in get_random_index():
                card[row][i]=0

        # print(card)
        self.card = card
        return self.card

    def print_card(self):
        '''

        :return: строка состоящую из 3 линий ячеек в строковм виде,
        '''
        def str2(x):
            if x==0:
                # если ноль то пробелы
                ret = '   '
            elif x < 0:
                # если число отрицательное (его зачеркнули) прочерк
                ret = ' - '
            elif x<10:
                # если однозначное число то пробел спереди
                ret = ' '+str(x)+' '
            else:
                # двузначные числа
                ret = str(x)+' '
            return ret

        ret=''
        for row in range(3):
            # проход по строкам
            for item in self.card[row]:
                # проход по колонкам
                ret += str2(item)
            ret+='\n'
        return ret

    def cross_cell(self, number):
        row,col = self.find_cell(number)
        if row >=0 and col>=0 :
            # число найдено
            self.card[row][col] *= -1 # делаю число отрицательным чтобы сохранить значение (для отладки),
                                  # печататься будет прочерк
            return True
        else:
            return False

    def find_cell(self,number):
        '''
        найти число в карточке
        :param number: число, которое ищем
        :return: кортеж (строка, колонка)
        '''
        for row in range(3):
            # проход по строкам
            for col in range(9):
                # проход по колонкам
                if self.card[row][col] == number:
                    return (row,col)
        return (-1,-1)

    def card_empty(self):
        '''
        проверяет есть ли ячейки > 0
        :return: True если нет таких ячеек, False наоборот
        '''
        for row in range(3):
            for col in range(9):
                if self.card[row][col] > 0:
                    return False
        return True

class Player():
    '''
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
    '''

    def __init__(self, itiscomp=1, name='Computer'):
        self.card = Card()
        self.name = name
        self.itiscomp = itiscomp
        self.status = 0

        def set_name(self):
            name = input(f'Имя человека {self.name} Введите новое имя (до 20 символов) или оставьте прежним (Enter) ')
            # берем первые 20 символов, если пустое имя - Player
            self.name = name[:20] if name else 'Player'

        def set_itiscomp(self):
            itiscomp = input(f'Это человек? Enter - Да, любой символ - Нет ')
            self.itiscomp = 0 if itiscomp else 1

        if not name : # если имя не задано
            set_name(self)

        if not itiscomp : # если не компьютер и имя не задано
            set_itiscomp()

    def set_status(self, status):
        self.status = status

    def info(self):
        print(f'{ITISCOMP[self.itiscomp]} {self.name}. Статус {STATUS[self.status]}. Карта: ')
        print(self.card.print_card())

    def check_step(self,barrel,step):
        # проверка верно или нет сделан ход и
        # установка статуса проиграл если ошибся
        # установка статуса выиграл если зачеркнул последнее число на карточке
        if step:  # реакция : надо зачеркнуть
            checked = 0 if self.card.find_cell(barrel) == (-1, -1) else 1  # проверку прошел# / не  прошел
        else:  # реакция : не надо зачеркнуть
            checked = 1 if self.card.find_cell(barrel) == (-1, -1) else 0  # проверку не прошел# /  прошел

        if checked:
            if self.card.find_cell(barrel) != (-1, -1):
                self.card.cross_cell(barrel)
                if self.card.card_empty():
                    self.status = 1
        else:  # проверку не прошел - проиграл
            self.status = -1
