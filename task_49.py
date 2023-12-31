'''
Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате .txt. Фамилия, имя, отчество, номер
телефона - данные, которые должны находиться
в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в
текстовом файле
3. Пользователь может ввести одну из
характеристик для поиска определенной
записи(Например имя или фамилию
человека)
4. Использование функций. Ваша программа
не должна быть линейной
'''

from os.path import exists
from csv import DictReader, DictWriter

class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt

class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt

def get_info():
    is_valid_first_name = False
    while not is_valid_first_name:
        try:
            first_name = input('Введите имя: ')
            if len(first_name) < 2:
                raise NameError('Имя должно содержать больше 1 символа!')
            else:
                is_valid_first_name = True
        except NameError as err:
            print(err)
            continue

    is_valid_second_name = False
    while not is_valid_second_name:
        try:
            second_name = input('Введите фамилию: ')
            if len(second_name) < 2:
                raise NameError('Фамилия должна содержать больше 1 символа!')
            else:
                is_valid_second_name = True
        except NameError as err:
            print(err)
            continue

    is_valid_phone = False
    while not is_valid_phone:
        try:
            phone_number = int(input('Введите номер: '))
            if len(str(phone_number)) != 11:
                raise LenNumberError('Неверная длина номера!')
            else:
                is_valid_phone = True
        except ValueError:
            print('Невалидный номер!')
            continue
        except LenNumberError as err:
            print(err)
            continue

    return [first_name, second_name, phone_number]


def create_file(file_name):
    # Менеджер контекста - with
    with open(file_name, 'w', encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)


def write_file(file_name, lst):
    res = read_file(file_name)
    for el in res:
        if el['Телефон'] == str(lst[2]):
            print('Такой телефон уже есть!')
            return
    obj = {'Имя': lst[0], 'Фамилия': lst[1], 'Телефон': lst[2]}
    res.append(obj)
    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)

file_name = 'phone.csv'
new_file = 'new_phone.csv'

def main():
    while True:
        command = input('Введите команду: ')
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name, get_info())
        elif command == 'r':
            if not exists(file_name):
                print('Файл отсутствует, создайте его')
                continue
            print(read_file(file_name))
        elif command == 'c':
            if not exists(file_name):
                print('Отсутствует основной файл, создайте его!')
                continue
            line_number = int(input('Введите номер строки: '))
            copy_data(file_name, new_file, line_number)


def copy_data(file_name, new_file, line_number):
    if line_number < 1 or line_number > len(read_file(file_name)):
        print('Некорректный номер строки!')
        return
    copy_obj = read_file(file_name)[line_number - 1]
    create_file(new_file)
    with open(new_file, 'w', encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerow(copy_obj)


main()