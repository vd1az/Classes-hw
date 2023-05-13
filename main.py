from collections import UserDict

class Field:
    def __init__(self, value) -> None:
        self.value = value

class Name(Field):
    ...


class Phone(Field):
    def make_list(self, phones: str):
        phones = phones.split(' ')
        return phones


class Record(Field):
    def __init__(self, name: Name, phone: Phone | str | None = None, phones: list[Phone] = []):
        self.name = name
        self.phones = phones
        if phone is not None:
            self.add_phone(phone)

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

    def get_name(self):
        return self.name.value


class AddressBook(UserDict, Field):

    def __init__(self, record: Record | None = None) -> None:
        self.records = {}
        if record is not None:
            self.add_record(record)

    def add_record(self, record: Record):
        self.records[record.get_name()] = record

    def show_adb(self):
        for name, record in self.records.items():
            print(f'{name}:')
            record.show_rec()
        return 'These are all your contacts.'

    def get_records(self, name: str):
        return self.records[name]


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


contacts = AddressBook()


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

exit_command = ['goodbye', 'close', 'exit', '.']

dict_of_commands = {'add': add,
                    'change': change,
                    'phone': phone,
                    'hello': hello,
                    'show': show}

while True:
    command, *date = input('Enter command: ').strip().split(' ', 1)
    command = command.lower()

    if command in exit_command:
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