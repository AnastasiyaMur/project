import re
import pandas as pd
import os


class Menu:
    def __init__(self):
        """Функция создаёт новые объекты класса - валидаторы,
        исходящее сообщение (появляется на экране пользователя при условии, что он ввёл нужные данные),
        ссобщение об ошибке, action( здесь содержутся действия,которые должна выполнить программа,если всё ок.
        """
        self.validators = [
            [lambda n: n in ['1', '2', '3', '4', '5']], #Функция проверяет, чтобы введенное пользователем число было из промежутка от 1 до 5 включительно
            [
                lambda name: re.fullmatch('[a-zA-Zа-яА-Я\.\- ]{5,40}', name), #Функция проверяет строку на соответствие шаблону и возвращает ее  в случае соответсвия
                lambda title: re.fullmatch('[a-zA-Zа-яА-Я\.\- 0-9]{1,50}', title), #Функция проверяет строку на соответствие шаблону и возвращает ее  в случае соответсвия
                lambda year: re.fullmatch('\-?[0-9]{,4}', year), #Функция проверяет строку на соответствие шаблону и возвращает ее  в случае соответсвия
                lambda publisher: re.fullmatch('[a-zA-Zа-яА-Я0-9 \.\-,:]{3,100}', publisher), #Функция проверяет строку на соответствие шаблону и возвращает ее  в случае соответсвия
                lambda isbn: re.fullmatch('[0-9]{1,6}\-[0-9]{1,6}\-[0-9]{1,6}\-[0-9]{1,6}\-[0-9]{1,6}', isbn) #Функция проверяет строку на соответствие шаблону и возвращает ее  в случае соответсвия
            ],
            [lambda file_name: file_name[-4:] == '.csv' and os.path.isfile(file_name)], #Функция проверяет, заканчивается ли имя файла на .csv и существует ли файл
            [lambda file_name: file_name[-4:] == '.csv' and not os.path.isfile(file_name)], #Функция проверяет, заканчивается ли имя файла на .csv и не существует ли файл
            [lambda sorting: sorting in ['1', '2']] #Функция проверяет, сортируются ли книги по критерию 1 или 2
        ]
        self.output_message = [
            [("Главное меню.\n"
               "Выберите цифру от 1 до 5.\n"
               "1. Добавить новую книгу. \n"
               "2. Загрузить книги из файла.\n"
               "3. Сохранить книги в файл. \n"
               "4. Отсортировать книги.\n"
               "5. Отобразить таблицу книг.\n"
               "Q. Выход. (работает на любом этапе программы)\n")],
            [
                "Введите имя автора",
                "Введите имя книги",
                "Введите год издания",
                "Введите название издательства",
                "Введите ISBN"
            ],
            ["Введите название файла. Должно заканчиваться на '.csv'. Такой файл должен существовать."],
            ["Введите название файла. Должно заканчиваться на '.csv'. Такой файл не должен существовать."],
            ["Выберите, как отсортировать. По году издания (1) или по алфавиту (2)."],
        ]
        self.error_message = [
            ["Не вводите всякую фигню ,кроме цифр от 1 до 5."],
            [
                "Можно вводить только буквы, точки либо дефис.",
                "Можно вводить только буквы, цифры точки либо дефис.",
                "Можно вводить только знак 'минус', цифры, количество которых не превышает 4",
                'Чота пошло криво!?!?',
                'Можно вводить только пять групп цифр через дефис. Пример: 978-2-266-11156-0.'
            ],
            ["Неправильно введено название файла."],
            ["Неправильно введено название файла."],
            [""]
        ]
        self.actions = [
            [self.__checkout_to_branch],
            [
                self.__set_author,
                self.__set_title,
                self.__set_year,
                self.__set_publisher,
                self.__set_isbn,
            ],
            [self.__open_books],
            [self.__save_books],
            [self.__sort_books],
        ]
        self.table = pd.DataFrame(columns=["title", 'author', 'year', 'publisher', 'isbn'])
        self.new_book = {'title': None, 'author': None, 'year': None, 'publisher': None, 'isbn': None}
        self.branch = 0
        self.phase = 0


    help(__init__)


    def __open_books(self, filename):
        """
        Функция открывает таблицу с загруженными книгами и возвращается в главное меню
        :param filename: имя файла
        """
        self.table = pd.read_csv(filename, index_col=False, header=0)
        self.phase = 0
        self.branch = 0


    help(__open_books)


    def __save_books(self, filename):
        """
        Функция сохраняет книги в таблицу и возвращается в главное меню
        :param filename: имя файла
        """
        self.table.to_csv(filename, index=False)
        self.phase = 0
        self.branch = 0


    help(__save_books)


    def __sort_books(self, option):
        """
        Функция сортирует книги по году либо по названию и возвращается в главное меню
        :param option: критерий, по которому сортируются книги
        """
        if option == '1':
            self.table = self.table.sort_values('year')
        elif option == '2':
            self.table = self.table.sort_values('title')
        self.phase = 0
        self.branch = 0


    help(__sort_books)


    def __checkout_to_branch(self, n):
        """
        Функция проверяет на какой ветке находится пользователь
        :param n: число,обозначающее ветку, на которой находится пользователь
        """
        self.branch = int(n)


    help(__checkout_to_branch)


    def __set_title(self, title):
        """
        Функция в будущую книгу в её поле title записывает то, что человек вводит с клавиатуры на данном этапе, и переходит на следующую фазу
        :param title: данные о названии книги,которые ввёл пользователь
        """
        self.new_book['title'] = title
        self.phase += 1


    help(__set_title)


    def __set_author(self, author):
        """
        Функция в будущую книгу в её поле author записывает то, что человек вводит с клавиатуры на данном этапе, и и переходит на следующую фазу
        :param author: данные об авторе книги,которые ввёл пользователь
        """
        self.new_book['author'] = author
        self.phase += 1


    help(__set_author)


    def __set_publisher(self, publisher):
        """
        Функция в будущую книгу в её поле publisher записывает то, что человек вводит с клавиатуры на данном этапе, и и переходит на следующую фазу
        :param publisher: данные об издательстве книги,которые ввёл пользователь
        """
        self.new_book['publisher'] = publisher
        self.phase += 1


    help(__set_publisher)


    def __set_year(self, year):
        """
        Функция в будущую книгу в её поле year записывает то, что человек вводит с клавиатуры на данном этапе, и и переходит на следующую фазу
        :param year:  данные о годе издания книги книги,которые ввёл пользователь
        """
        self.new_book['year'] = int(year)
        self.phase += 1


    help(__set_year)

    def __set_isbn(self, isbn):
        """
        Функция в будущую книгу в её поле isbn записывает то, что человек вводит с клавиатуры на данном этапе, и и переходит в глваное меню
        :param isbn: данные о isbn книги книги,которые ввёл пользователь
        """
        self.new_book['isbn'] = isbn
        self.table = pd.concat([self.table, pd.DataFrame.from_records([self.new_book])], ignore_index=True)
        self.phase = 0
        self.branch = 0


    help(__set_isbn)


    def process_answer(self, answer):
        """
        Функция, обрабатывающая введенные пользователем данные
        :param answer: введенный пользователем ответ
        :return: false, если введены q/Q,
                открывает таблицу, если введено "5"
                перебрасывает на следующую соответсвующую ветку и фазу, если введено все, кроме й/q и "5"
                иначе возвращает соответствующее сообщение об ошибке
        """
        if answer in ['q', 'Q']:
            return False
        if answer == '5':
            return self.table
        elif self.validators[self.branch][self.phase](answer):
            self.actions[self.branch][self.phase](answer)
            return self.output_message[self.branch][self.phase]
        else:
            return self.error_message[self.branch][self.phase]


    help(process_answer)


    def run(self):
        "Функция, печатающая исходящее сообщение соответсвующих ветки и фазы, до тех пор пока введенные пользователем данные корректны, иначе выводит результат."
        print(self.output_message[self.branch][self.phase])
        while True:
            answer = input(": ")
            res = self.process_answer(answer)
            if res is False:
                break
            print(res)


    help(run)

    def run_as_robot(self, message):
        """
        Функция, запускающая робота, который имитирует пользователя.
        :param message: сообщение введенное роботом с консоли
        :return: проанализированный ппограммой ответ
        """
        if message == r'\restart':
            self.branch = 0
            self.phase = 0
        return self.process_answer(message)

    help(run_as_robot)


def test_adding_book():
    "Функция, тестирующая возможность создания новой книги. Проверяет выводится ли на введенные данные соответсвующее исходное сообщение/ сообщение об ошибке"
    m = Menu()
    # Main menu - choosing add page
    assert m.run_as_robot('1') == m.output_message[1][0]


    # book author
    assert m.run_as_robot('123456') == m.error_message[1][0]
    assert m.run_as_robot('!@#$') == m.error_message[1][0]
    assert m.run_as_robot('Nastya') == m.output_message[1][1]

    # book title
    assert m.run_as_robot('!@#$%') == m.error_message[1][1]
    assert m.run_as_robot('1234') == m.output_message[1][2]

    # book year
    assert m.run_as_robot('asdfsg') == m.error_message[1][2]
    assert m.run_as_robot('12345678') == m.error_message[1][2]
    assert m.run_as_robot('-123456') == m.error_message[1][2]
    assert m.run_as_robot('1-6') == m.error_message[1][2]
    assert m.run_as_robot('1998') == m.output_message[1][3]

    # book publisher
    assert m.run_as_robot('1') == m.error_message[1][3]
    assert m.run_as_robot('@#$%^f') == m.error_message[1][3]
    assert m.run_as_robot('Росмэн') == m.output_message[1][4]

    # ISBN
    assert m.run_as_robot('12345') == m.error_message[1][4]
    assert m.run_as_robot('f-f-f-f-f') == m.error_message[1][4]
    assert m.run_as_robot('123456789-9876543211-23456789-98765432-12345678') == m.error_message[1][4]
    assert m.run_as_robot('1234-1234-4321-4312-2386') == m.output_message[0][0]


help(test_adding_book)


def test_read_file():
    "Функция, тестирующая возможность загрузки уже существующей книги."
    m = Menu()
    assert m.run_as_robot('q') is False
    m = Menu()
    with open('lola.csv', 'w') as file:
        file.write('a,b,c,d\n1,2,3,4')
    assert m.run_as_robot('2') == m.output_message[2][0]
    assert m.run_as_robot('098765432') == m.error_message[2][0]
    assert m.run_as_robot('.jpg') == m.error_message[2][0]
    assert m.run_as_robot('.csv') == m.error_message[2][0]
    assert m.run_as_robot('lola.csv') == m.output_message[0][0]
    os.remove('lola.csv')


help(test_read_file)

def test_saved_file():
    "Функция, тестирующая возможность сохранения книги."
    m = Menu()
    m.run_as_robot('1')
    m.run_as_robot('Nastya')
    m.run_as_robot('kniga')
    m.run_as_robot('2005')
    m.run_as_robot('Yaghj')
    m.run_as_robot('1-1-1-1-1')
    assert m.run_as_robot('3') == m.output_message[3][0]
    os.remove('filename.csv')
    assert m.run_as_robot('filename.csv') == m.output_message[0][0]

    with open('filename.csv', 'r') as file:
        content = file.read()
    answer = 'title,author,year,publisher,isbn\nkniga,Nastya,2005,Yaghj,1-1-1-1-1\n'
    assert content == answer
    os.remove('filename.csv')


help(test_saved_file)


def test_sorted_file():
    "Функция, тестирующая возможность сортировки книг."
    header = 'title,author,year,publisher,isbn\n'
    row1 = 'Book,Nastya,2005,Me n Myself,1-1-1-1-1\n'
    row2 = 'Author book,Nastya,2006,Me n myself,1-1-1-1-1\n'

    with open('filename.csv', 'w') as file:
        file.write(header+row1+row2)
    df = pd.read_csv('filename.csv')
    m = Menu()
    m.run_as_robot('2')
    m.run_as_robot('filename.csv')
    assert m.run_as_robot('4') == m.output_message[4][0]
    assert m.run_as_robot('1') == m.output_message[0][0]
    assert str(m.run_as_robot('5')) == str(df.sort_values('year'))
    assert m.run_as_robot('4') == m.output_message[4][0]
    assert m.run_as_robot('2') == m.output_message[0][0]
    assert str(m.run_as_robot('5')) == str(df.sort_values('title'))


help(test_sorted_file)

test_adding_book()
test_read_file()
test_saved_file()
test_sorted_file()

m = Menu()
m.run()