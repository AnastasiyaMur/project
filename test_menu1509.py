from menu1509 import Menu
import pandas as pd
import unittest
import os


class MenuTest(unittest.TestCase):
    def test_adding_book(self):
        "Функция, тестирующая возможность создания новой книги. Проверяет выводится ли на введенные данные соответсвующее исходное сообщение/ сообщение об ошибке"
        m = Menu()
        # Main menu - choosing add page
        self.assertTrue(m.run_as_robot('1') == m.output_message[1][0])

        # book author
        self.assertTrue(m.run_as_robot('123456') == m.error_message[1][0])
        self.assertTrue(m.run_as_robot('!@#$') == m.error_message[1][0])
        self.assertTrue(m.run_as_robot('Nastya') == m.output_message[1][1])

        # book title
        self.assertTrue(m.run_as_robot('!@#$%') == m.error_message[1][1])
        self.assertTrue(m.run_as_robot('1234') == m.output_message[1][2])

        # book year
        self.assertTrue(m.run_as_robot('asdfsg') == m.error_message[1][2])
        self.assertTrue(m.run_as_robot('12345678') == m.error_message[1][2])
        self.assertTrue(m.run_as_robot('-123456') == m.error_message[1][2])
        self.assertTrue(m.run_as_robot('1-6') == m.error_message[1][2])
        self.assertTrue(m.run_as_robot('1998') == m.output_message[1][3])

        # book publisher
        self.assertTrue(m.run_as_robot('1') == m.error_message[1][3])
        self.assertTrue(m.run_as_robot('@#$%^f') == m.error_message[1][3])
        self.assertTrue(m.run_as_robot('Росмэн') == m.output_message[1][4])

        # ISBN
        self.assertTrue(m.run_as_robot('12345') == m.error_message[1][4])
        self.assertTrue(m.run_as_robot('f-f-f-f-f') == m.error_message[1][4])
        self.assertTrue(m.run_as_robot('123456789-9876543211-23456789-98765432-12345678') == m.error_message[1][4])
        self.assertTrue(m.run_as_robot('1234-1234-4321-4312-2386') == m.output_message[0][0])
        

    def test_read_file(self):
        "Функция, тестирующая возможность загрузки уже существующей книги."
        m = Menu()
        self.assertTrue(m.run_as_robot('q') is False)
        m = Menu()
        with open('lola.csv', 'w') as file:
            file.write('a,b,c,d\n1,2,3,4')
        self.assertTrue(m.run_as_robot('2') == m.output_message[2][0])
        self.assertTrue(m.run_as_robot('098765432') == m.error_message[2][0])
        self.assertTrue(m.run_as_robot('.jpg') == m.error_message[2][0])
        self.assertTrue(m.run_as_robot('.csv') == m.error_message[2][0])
        self.assertTrue(m.run_as_robot('lola.csv') == m.output_message[0][0])
        os.remove('lola.csv')


    def test_saved_file(self):
        "Функция, тестирующая возможность сохранения книги."
        m = Menu()
        m.run_as_robot('1')
        m.run_as_robot('Nastya')
        m.run_as_robot('kniga')
        m.run_as_robot('2005')
        m.run_as_robot('Yaghj')
        m.run_as_robot('1-1-1-1-1')
        self.assertTrue(m.run_as_robot('3') == m.output_message[3][0])
        self.assertTrue(m.run_as_robot('filename.csv') == m.output_message[0][0])

        with open('filename.csv', 'r') as file:
            content = file.read()
        answer = 'title,author,year,publisher,isbn\nkniga,Nastya,2005,Yaghj,1-1-1-1-1\n'
        self.assertTrue(content == answer)
        os.remove('filename.csv')


    def test_sorted_file(self):
        "Функция, тестирующая возможность сортировки книг."
        header = 'title,author,year,publisher,isbn\n'
        row1 = 'Book,Nastya,2005,Me n Myself,1-1-1-1-1\n'
        row2 = 'Author book,Nastya,2006,Me n myself,1-1-1-1-1\n'

        with open('filename.csv', 'w') as file:
            file.write(header + row1 + row2)
        df = pd.read_csv('filename.csv')
        m = Menu()
        m.run_as_robot('2')
        m.run_as_robot('filename.csv')
        self.assertTrue(m.run_as_robot('4') == m.output_message[4][0])
        self.assertTrue(m.run_as_robot('1') == m.output_message[0][0])
        self.assertTrue(str(m.run_as_robot('5')) == str(df.sort_values('year')))
        self.assertTrue(m.run_as_robot('4') == m.output_message[4][0])
        self.assertTrue(m.run_as_robot('2') == m.output_message[0][0])
        self.assertTrue(str(m.run_as_robot('5')) == str(df.sort_values('title')))
        os.remove('filename.csv')

