# Функція для додавання контакту
def add_contact(name, address, phone, email, birthday):
    if not validate_phone_number(phone):
        print("Некоректний номер телефону. Будь ласка, введіть у форматі +X (XXX) XXX-XX-XX.")
        return
    if not validate_email(email):
        print("Некоректна електронна пошта. Будь ласка, введіть дійсну адресу електронної пошти.")
        return

    contacts = read_data(CONTACTS_FILE)
    contacts.append({
        "name": name,
        "address": address,
        "phone": phone,
        "email": email,
        "birthday": birthday
    })
    write_data(contacts, CONTACTS_FILE)

# Функція для редагування контакту за іменем
def edit_contact(name, new_data):
    contacts = read_data(CONTACTS_FILE)
    for contact in contacts:
        if contact["name"] == name:
            # Перевірка правильності нових даних перед зміною
            if "phone" in new_data and not validate_phone_number(new_data["phone"]):
                print("Некоректний номер телефону. Будь ласка, введіть у форматі +X (XXX) XXX-XX-XX.")
                return
            if "email" in new_data and not validate_email(new_data["email"]):
                print("Некоректна електронна пошта. Будь ласка, введіть дійсну адресу електронної пошти.")
                return

            contact.update(new_data)
            break
    write_data(contacts, CONTACTS_FILE)
