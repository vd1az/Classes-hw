from collections import UserDict
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
import pickle

class Field:
    def __init__(self, value) -> None:
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

class Name(Field):
    def __init__(self, name: str) -> None:
        self.value = name

    @Field.value.setter
    def value(self, name):
        if len(name) > 1:
            Field.value.fset(self, name)
        else:
            raise ValueError("There must be a name")


class Phone(Field):
    def __init__(self, phone):
        self.value = phone

    @Field.value.setter
    def value(self, phone):
        if phone.replace(' ', '').isdigit():
            Field.value.fset(self, phone)
        else:
            raise ValueError("Enter the numbers")
    def make_list(self, phones: str):
        phones = phones.split(' ')
        return phones


class Birthday(Field):
    def __init__(self, birthday):
        self.value = birthday
        self.birthday = self.value.replace(year=datetime.now().year)

    @Field.value.setter
    def value(self, birthday):
        try:
            dt = datetime.strptime(birthday, '%d.%m.%Y')
        except (ValueError, TypeError):
            raise Exception("Plz enter birthday format as dd.mm.yyyy")
        Field.value.fset(self, dt.date())

    def days_to_birthday(self):
        self.birthday = datetime.combine(self.birthday, datetime.min.time())

        if (self.birthday - datetime.now()).days >= 0:
            return (self.birthday - datetime.now()).days
        else:
            if datetime.now().year % 4:
                return (self.birthday - datetime.now()).days + 365 + 1
            else:
                return (self.birthday - datetime.now()).days + 366 + 1


class Record(Birthday, Field):
    def __init__(self, name: Name, phone: Phone | str | None = None, phones: list[Phone] = [], birthday: str = None):
        if birthday is not None:
            super().__init__(birthday)
        self.name = name
        self.phones = phones
        if phone is not None:
            self.add_phone(phone)

    def get_birthday(self):
        return f"{self.birthday.day}.{self.birthday.month}.{self.value.year}"

    def add_phone(self, phone: Phone | str):
        if isinstance(phone, str):
            phone = self.create_phone(phone)
        self.phones.append(phone)

    def create_phone(self, phone: str):
        return Phone(phone)

    def change_phone(self, new_phone):
        self.phones = new_phone


    def show_rec(self):
        for indx, phone in enumerate(self.phones):
            print(f'{indx + 1}: {phone.value}')

    def show_phones(self):
        cont = []
        for phone in self.phones:
            cont.append(phone.value)
        return cont

    def get_name(self):
        return self.name.value


class Iterator:
    def __init__(self, n_rec, adbook):
        self.n_rec = n_rec
        self.index = 0
        self.adbook = adbook

    def __next__(self):
        if self.index <= len(self.adbook):
            res = ''
            for name, numbers, birthday in self.adbook[self.index:self.n_rec]:
                if birthday == None:
                    res += f"{name}: {numbers}\n"
                else:
                    res += f"{name}: {numbers}\t{name}`s birthday: {birthday}\n"
            self.index = self.n_rec
            self.n_rec += self.n_rec

            return res
        else:
            raise StopIteration


class AddressBook(UserDict, Field):
    def __init__(self, filename, record: Record | None = None, n_rec=5) -> None:
        self.n_rec = n_rec
        self.records = {}
        self.file = Path(filename)
        self.deserialize()
        if record is not None:
            self.add_record(record)

    def add_record(self, record: Record):
        self.records[record.get_name()] = record

    def search(self, search_str: str):
        result = {}
        for name, record in self.records.items():
            if search_str in name or ','.join(record.show_phones()).__contains__(search_str):
                result[name] = record.show_phones()
        return result

    def show_adb(self):
        for name, record in self.records.items():
            print(f'{name}:')
            record.show_rec()
            try:
                print(f"{name}`s birthday: {record.get_birthday()}")
            except:
                pass
        return 'All your contacts.'

    def serialize(self):
        with open(self.file, "wb") as file:
            pickle.dump(self.records, file)

    def deserialize(self):
        if not self.file.exists():
            return None
        try:
            with open(self.file, "rb") as file:
                self.records = pickle.load(file)
        except EOFError:
            return None



    def get_tuple(self):
        res = []
        for name, record in self.records.items():
            try:
                res.append((name, record.show_phones(), record.get_birthday()))
            except:
                res.append((name, record.show_phones(), None))
        return res

    def get_records(self, name: str):
        return self.records[name]

    def add_n_rec(self, n_rec: int) -> None:
        self.n_rec = n_rec

    def __iter__(self) -> Iterator:
        return Iterator(n_rec=self.n_rec, adbook=self.get_tuple())


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact is missing.'
        except ValueError:
            return 'Write numbers as phone please.'
        except IndexError:
            return 'Give me name and phone please.'
        except TypeError:
            return 'Error of arguments in function.'
    return inner


contacts = AddressBook('adress.bin')


def hello():
    return 'How can I help you?'


@input_error
def add(name: str, phone_number: str) -> str:
    name_ = Name(name)
    phones = Phone(phone_number)
    phones = phones.make_list(phone_number)
    phones = [Phone(val) for val in phones]
    record = Record(name=name_, phones=phones)
    contacts.add_record(record)
    return f'Done, contact is saved.'


@input_error
def change(name: str, new_phone: str) -> str:
    record = contacts.get_records(name)
    phones = Phone(new_phone)
    phones = phones.make_list(new_phone)
    phones = [Phone(val) for val in phones]
    record.change_phone(phones)
    return 'Done, number is changed.'


@input_error
def phone(name: str) -> str:
    res = contacts.get_records(name)
    res.show_rec()
    return f'These are {name}\'s phone numbers.'


def show() -> str:
    if len(contacts.records) == 0:
        return 'You have not any contacts.'
    else:
        return contacts.show_adb()


@input_error
def iterator(n_rec: int) -> str:
    if len(contacts.records) == 0:
        return 'You have not any contacts.'
    else:
        contacts.add_n_rec(int(n_rec))
        for i in contacts:
            print(i)
        return 'These are all contacts.'


@input_error
def birthday(name: str) -> str:
    try:
        a = contacts.get_records(name)
        return a.days_to_birthday()
    except:
        return 'No birthday found'


@input_error
def search(value: str) -> str:
    if contacts.search(value) != {}:
        return contacts.search(value)
    return 'There is nothing.'

exit_command = ['goodbye', 'close', 'exit', '.']

dict_of_commands = {'add': add,
                    'change': change,
                    'phone': phone,
                    'hello': hello,
                    'show': show,
                    'iterator': iterator,
                    'birthday': birthday,
                    'search': search
                    }

while True:
    command, *date = input('Enter command: ').strip().split(' ', 1)
    command = command.lower()

    if command in exit_command:
        contacts.serialize()
        print('Good bye!')
        break

    elif dict_of_commands.get(command):
        handler = dict_of_commands.get(command)
        if date:
            date = date[0].split(', ')
            print(handler(*date))
        else:
            print(handler())

    else:
        print('Unknown command!')