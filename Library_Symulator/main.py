from requests import get
import json
from datetime import datetime
import names


def restart_books_data():
    query = get("https://wolnelektury.pl/api/books/")

    all_books = []

    # Loop through the books and append each to the all_books list
    for book_id, book in enumerate(query.json(), start=1):
        data = {
            "book_id": book_id,
            "title": book["title"],
            "borrowed": False
        }
        all_books.append(data)

    # Write the updated list of books back to the file in UTF-8 encoding
    with open('books.json', 'w', encoding='utf-8') as file:
        json.dump(all_books, file, ensure_ascii=False, indent=4)


def generate_names(n):
    return [(names.get_first_name(), names.get_last_name()) for _ in range(n)]


def restart_user_data():
    all_users = []
    names_list = generate_names(100)
    for user_id, (first_name, last_name) in enumerate(names_list, start=1):
        data = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "debt": 0,
            "books": None
        }
        all_users.append(data)

    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(all_users, file, ensure_ascii=False, indent=4)


# Function to add books to a specific user
def add_books_to_user(user_id, new_book):
    # Read the JSON file
    with open('users.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Iterate through the users to find the matching user_id
    for user in data:
        if user['user_id'] == user_id:
            # If books is None, initialize it as an empty list
            if user['books'] is None:
                user['books'] = []
            # Add new books to the user's books list
            if new_book not in user["books"]:
                user['books'].append(new_book)
            break

    # Write the updated data back to the JSON file
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def del_book_to_user(user_id, id_book):
    # Read the JSON file
    with open('users.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Iterate through the users to find the matching user_id
    for user in data:
        if user['user_id'] == user_id:
            # If books is None, initialize it as an empty list
            if user["books"][int(id_book) - 1] in user['books']:
                user['books'].remove(user["books"][int(id_book) - 1])
            break

    # Write the updated data back to the JSON file
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def set_book_borrowed(book_id):
    with open('books.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for book in data:
        if book['book_id'] == book_id:
            book["borrowed"] = True

    with open('books.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def set_book_unborrowed(book_id):
    with open('books.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for book in data:
        if book['book_id'] == book_id:
            book["borrowed"] = False

    with open('books.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def set_book_unborrowed_title(title):
    with open('books.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for book in data:
        if book['title'] == title:
            book["borrowed"] = False

    with open('books.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def add_user_debt(user_id, debt):
    with open('users.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for user in data:
        if user['user_id'] == user_id:
            user["debt"] += int(debt)

    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def del_user_debt(user_id, debt):
    with open('users.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for user in data:
        if user['user_id'] == user_id:
            user["debt"] -= int(debt)
        if user["debt"] < 0:
            napiwek = abs(user["debt"])
            user["debt"] = 0
    if user["debt"] == 0:
        print("Debet splacony ")
        if napiwek != 0:
            print(f"Dziekujemy za napwiek w wysokosci {napiwek}")
    else:
        print(f"Pozostaje jeszcze {user["debt"]} do zaplaty")
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)





def calculate_months(start_date_str, end_date_str, date_format="%d-%m-%Y"):
    start_date = datetime.strptime(start_date_str, date_format)
    end_date = datetime.strptime(end_date_str, date_format)

    year_diff = end_date.year - start_date.year
    month_diff = end_date.month - start_date.month

    total_months = year_diff * 12 + month_diff

    return total_months


def show_users():
    with open('users.json', 'r', encoding='utf-8') as file:
        users = json.load(file)
    for user in users:
        print(f"{user["user_id"]}.{user["first_name"]} {user["last_name"]}")
    return users

def show_avaiable_books():
    with open('books.json', 'r', encoding='utf-8') as file:
        books = json.load(file)
    for book in books:
        if not book["borrowed"]:
            print(f"{book['book_id']}. {book['title']}")


def wypozyczanie_ksiazki():
    with open('users.json', 'r', encoding='utf-8') as file:
        users = json.load(file)
    with open('books.json', 'r', encoding='utf-8') as file:
        books = json.load(file)
    for user in users:
        print(f"{user["user_id"]}.{user["first_name"]} {user["last_name"]}")
    search_user_id = int(input("Wybierz uzytkownika:"))
    for book in books:
        print(f"{book["book_id"]}.{book["title"]}")
    search_book_id = int(input("Wybierz ksiazke:"))
    found_book_title = next(filter(lambda x: x["book_id"] == search_book_id, books))

    if not found_book_title["borrowed"]:
        add_books_to_user(search_user_id, found_book_title["title"])
        set_book_borrowed(search_book_id)

    else:
        print("Ksiazka niedostepna")


def oddanie_ksiazki():
    with open('users.json', 'r', encoding='utf-8') as file:
        users = json.load(file)

    for user in users:
        print(f"{user["user_id"]}.{user["first_name"]} {user["last_name"]}")
    search_user_id = int(input("Wybierz uzytkownika:"))
    for user in users:
        if user['user_id'] == search_user_id:
            if user['books'] is None or not user['books']:
                print(f"Uzytkownik  {user["first_name"]} {user["last_name"]} nie wypozyczyl ksiazek")
            else:
                while True:
                    for id, book in enumerate(user["books"], start=1):
                        print(f"{id}.{book}")
                    id_book = int(input("Wybierz ksiazke: "))
                    if id_book <= len(user["books"]):
                        break
                data_wypozyczenia = input("Podaj date wypozyczenia: dd-mm-YYYY")
                data_oddania = input("Podaj date oddania: dd-mm-YYYY")
                miesiace = calculate_months(data_wypozyczenia, data_oddania)
                print(f"Uzytkownik {user["first_name"]} {user["last_name"]} oddal ksiazke po czasie {miesiace} m.")
                if miesiace > 2:
                    debt = 5 + 5 * (miesiace - 2)
                else:
                    debt = 5
                print(f"Debet o wysokosci {debt} zostal dodany")
                add_user_debt(search_user_id, debt)
                del_book_to_user(search_user_id, id_book)
                set_book_unborrowed_title(user["books"][id_book - 1])


while True:
    print(
        "\n1.Wyswietl dostepne ksiazki \n2.Wyswietl informacje o uztkownikach\n3.Wypozyczenie ksiazki przez uzytkownika\n4.Zwrot ksiazki\nQuit")
    option = input("\nCo chcesz zrobic ")
    if option == "1":
        show_avaiable_books()
    elif option == "2":
        while True:
            users = show_users()
            id_user = int(input("Wybierz uzytkownika "))
            if id_user <= len(users):
                break
        for user in users:
            if user["user_id"] == id_user:
                print(f"\nImie: {user["first_name"]}\n"
                      f"Nazwisko: {user["last_name"]}\n"
                      f"Debet: {user["debt"]}\n")
        while True:
            dec = input("Czy chcesz zaplacic debet? T/N")
            if dec.lower() == "t":
                debt = int(input("Ile chcesz zaplacic? "))
                del_user_debt(id_user,debt)
                break
            if dec.lower() == "n":
                break
            else:
                print("WHot https://www.youtube.com/watch?v=o4PfOudBB4U")

    elif option == "3":
        wypozyczanie_ksiazki()
    elif option == "4":
        oddanie_ksiazki()
    elif option.lower() == "quit" or option == "5":
        print("Koniec programu.")
        break
    else:

        print("Nieprawidłowa opcja. Proszę wybrać ponownie.")
