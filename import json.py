import json
import os

class User:
    def __init__(self, username, password, role):
        self.__username = username
        self.__password = password
        self.__role = role
        self.__history = []

    def buy_item(self, item):
        self.__history.append(item)

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_role(self):
        return self.__role

    def get_history(self):
        return self.__history


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, role='admin')
        self.__items = []

    def add_item(self, item):
        self.__items.append(item)
        self.save_items()  

    def remove_item(self, item):
        self.__items.remove(item)
        self.save_items()  

    def modify_item(self, item, new_item):
        index = self.__items.index(item)
        self.__items[index] = new_item
        self.save_items()  

    def get_items(self):
        return self.__items

    def save_items(self):
        with open("items.txt", "w") as file:
            json.dump([item.to_dict() for item in self.__items], file)

    def load_items(self):
        if os.path.exists("items.txt"):
            with open("items.txt", "r") as file:
                items_data = json.load(file)
                self.__items = [Item(**data) for data in items_data]


class Item:
    def __init__(self, name, price, rarity):
        self.__name = name
        self.__price = price
        self.__rarity = rarity

    def __str__(self):
        return f"{self.__name} (Цена: {self.__price}, Редкость: {self.__rarity})"

    def to_dict(self):
        return {"name": self.__name, "price": self.__price, "rarity": self.__rarity}

    def get_name(self):
        return self.__name


class Marketplace:
    def __init__(self):
        self.__users = []
        self.__admin = Admin("admin", "admin123")
        self.__admin.load_items() 
        self.__current_user = None

    def register_user(self, username, password):
        if any(user.get_username() == username for user in self.__users):
            print("Пользователь с таким именем уже существует!")
        else:
            self.__users.append(User(username, password, role='user'))
            print(f"Пользователь {username} успешно зарегистрирован!")

    def login(self, username, password):
        if username == self.__admin.get_username() and password == self.__admin.get_password():
            self.__current_user = self.__admin
            print("Вход выполнен как администратор.")
            return True

        for user in self.__users:
            if user.get_username() == username and user.get_password() == password:
                self.__current_user = user
                print(f"Вход выполнен как пользователь {username}.")
                return True

        print("Неправильное имя пользователя или пароль.")
        return False

    def show_items(self):
        print("Доступные товары:")
        for item in self.__admin.get_items():
            print(item)

    def buy_item(self, item_name):
        for item in self.__admin.get_items():
            if item.get_name() == item_name:
                self.__current_user.buy_item(item)
                print(f"Вы купили: {item}")
                return
        print("Товар не найден!")

    def admin_menu(self):
        while True:
            print("Административное меню:")
            print("1. Добавить товар")
            print("2. Удалить товар")
            print("3. Изменить товар")
            print("4. Показать товары")
            print("0. Выйти")
            choice = input("Выберите опцию: ")

            if choice == '1':
                name = input("Введите имя товара: ")
                price = float(input("Введите цену товара: "))
                rarity = input("Введите редкость товара: ")
                self.__admin.add_item(Item(name, price, rarity))
                print(f"Товар {name} добавлен.")
            elif choice == '2':
                name = input("Введите имя товара, который хотите удалить: ")
                item_to_remove = next((item for item in self.__admin.get_items() if item.get_name() == name), None)
                if item_to_remove:
                    self.__admin.remove_item(item_to_remove)
                    print(f"Товар {name} удалён.")
                else:
                    print("Товар не найден.")
            elif choice == '3':
                name = input("Введите имя товара, который хотите изменить: ")
                item_to_modify = next((item for item in self.__admin.get_items() if item.get_name() == name), None)
                if item_to_modify:
                    new_name = input("Введите новое имя товара: ")
                    new_price = float(input("Введите новую цену товара: "))
                    new_rarity = input("Введите новую редкость товара: ")
                    new_item = Item(new_name, new_price, new_rarity)
                    self.__admin.modify_item(item_to_modify, new_item)
                    print(f"Товар {item_to_modify.get_name()} изменён на {new_item.get_name()}.")
                else:
                    print("Товар не найден.")
            elif choice == '4':
                self.show_items()
            elif choice == '0':
                break

    def user_menu(self):
        while True:
            print("Пользовательское меню:")
            print("1. Показать все товары")
            print("2. Купить товар")
            print("3. Посмотреть историю покупок")
            print("0. Выйти")
            choice = input("Выберите опцию: ")

            if choice == '1':
                self.show_items()
            elif choice == '2':
                item_name = input("Введите имя товара, который хотите купить: ")
                self.buy_item(item_name)
            elif choice == '3':
                print("Ваша история покупок:")
                if self.__current_user.get_history():
                    for item in self.__current_user.get_history():
                        print(item)
                else:
                    print("У вас нет купленных товаров.")
            elif choice == '0':
                break


def main():
    marketplace = Marketplace()

    while True:
        print("Главное меню:")
        print("1. Регистрация")
        print("2. Вход")
        print("0. Выход")
        choice = input("Выберите опцию: ")

        if choice == '1':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            marketplace.register_user(username, password)
        elif choice == '2':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            if marketplace.login(username, password):
                if marketplace._Marketplace__current_user.get_role() == 'admin':
                    marketplace.admin_menu()
                else:
                    marketplace.user_menu()
        elif choice == '0':
            break


if __name__ == "__main__":
    main()