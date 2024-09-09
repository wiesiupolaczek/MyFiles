from requests import get
import json
from datetime import datetime
import names
import random


class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.descriptions = [
            "A captivating tale of adventure and intrigue.",
            "Explore a world of mystery and wonder.",
            "A literary masterpiece that will stay with you long after you finish reading.",
            "Delve into the complexities of human nature.",
            "A journey of self-discovery and personal growth.",
            "A thrilling story that will keep you on the edge of your seat.",
            "Experience the power of love and forgiveness.",
            "A thought-provoking exploration of societal issues.",
            "A timeless classic that continues to resonate with readers today.",
            "A captivating blend of history and fiction.",
        ]

    def restart_books_data(self):
        query = get("https://wolnelektury.pl/api/books/")
        self.books = [{"book_id": book_id, "title": book["title"], "borrowed": False, "cover_url": book["simple_thumb"], "description": 7*random.choice(self.descriptions)}
                      for book_id, book in enumerate(query.json(), start=1)]
        self.save_books()

    def save_books(self):
        with open('books.json', 'w', encoding='utf-8') as file:
            json.dump(self.books, file, ensure_ascii=False, indent=4)

    def restart_user_data(self):
        self.users = [{"user_id": user_id, "first_name": first_name, "last_name": last_name, "debt": 0, "books": []}
                      for user_id, (first_name, last_name) in enumerate(self.generate_names(100), start=1)]
        self.save_users()

    def save_users(self):
        with open('users.json', 'w', encoding='utf-8') as file:
            json.dump(self.users, file, ensure_ascii=False, indent=4)

    def generate_names(self, n):
        return [(names.get_first_name(), names.get_last_name()) for _ in range(n)]

    def add_books_to_user(self, user_id, new_book):
        user = self.get_user(user_id)
        if user and new_book not in user["books"]:
            user["books"].append(new_book)
            self.save_users()

    def del_book_to_user(self, user_id, id_book):
        user = self.get_user(user_id)
        if user and user["books"]:
            if 0 < id_book <= len(user["books"]):
                del user["books"][id_book - 1]
                self.save_users()

    def set_book_borrowed(self, book_id):
        book = self.get_book(book_id)
        if book:
            book["borrowed"] = True
            self.save_books()

    def set_book_unborrowed(self, book_id):
        book = self.get_book(book_id)
        if book:
            book["borrowed"] = False
            self.save_books()

    def set_book_unborrowed_title(self, title):
        book = self.get_book_by_title(title)
        if book:
            book["borrowed"] = False
            self.save_books()

    def add_user_debt(self, user_id, debt):
        user = self.get_user(user_id)
        if user:
            user["debt"] += debt
            self.save_users()

    def del_user_debt(self, user_id, debt):
        user = self.get_user(user_id)
        if user:
            user["debt"] -= debt
            napiwek = 0
            if user["debt"] < 0:
                napiwek = abs(user["debt"])
                user["debt"] = 0
            self.save_users()
            if user["debt"] == 0:
                print("Debt paid off")
                if napiwek:
                    print(f"Thank you for the tip of {napiwek}")
            else:
                print(f"{user['debt']} remaining to be paid")

    def calculate_months(self, start_date_str, end_date_str, date_format="%d-%m-%Y"):
        start_date = datetime.strptime(start_date_str, date_format)
        end_date = datetime.strptime(end_date_str, date_format)
        year_diff = end_date.year - start_date.year
        month_diff = end_date.month - start_date.month
        return year_diff * 12 + month_diff

    def show_users(self):
        self.load_users()
        for user in self.users:
            print(f"{user['user_id']}. {user['first_name']} {user['last_name']}")
        return self.users

    def show_available_books(self):
        self.load_books()
        for book in self.books:
            if not book["borrowed"]:
                print(f"{book['book_id']}. {book['title']} - {book['description']}") # Display description here

    def borrow_book(self):
        self.load_users()
        self.load_books()
        for user in self.users:
            print(f"{user['user_id']}. {user['first_name']} {user['last_name']}")
        user_id = int(input("Select user: "))
        for book in self.books:
            print(f"{book['book_id']}. {book['title']} - {book['description']}") # Display description here
        book_id = int(input("Select book: "))
        found_book = self.get_book(book_id)
        if found_book and not found_book["borrowed"]:
            self.add_books_to_user(user_id, found_book["title"])
            self.set_book_borrowed(book_id)
        else:
            print("Book not available")

    def return_book(self):
        self.load_users()
        for user in self.users:
            print(f"{user['user_id']}. {user['first_name']} {user['last_name']}")
        user_id = int(input("Select user: "))
        user = self.get_user(user_id)
        if user and user["books"]:
            while True:
                for id, book in enumerate(user["books"], start=1):
                    print(f"{id}. {book}")
                id_book = int(input("Select book: "))
                if 0 < id_book <= len(user["books"]):
                    break
            borrow_date = input("Enter borrow date (dd-mm-YYYY): ")
            return_date = input("Enter return date (dd-mm-YYYY): ")
            months = self.calculate_months(borrow_date, return_date)
            print(f"{user['first_name']} {user['last_name']} returned the book after {months} months.")
            debt = 5 + 5 * (months - 2) if months > 2 else 5
            print(f"A debt of {debt} has been added")
            self.add_user_debt(user_id, debt)
            self.set_book_unborrowed_title(user["books"][id_book - 1])
            self.del_book_to_user(user_id, id_book)
        else:
            print(f"{user['first_name']} {user['last_name']} has not borrowed any books")

    def load_books(self):
        try:
            with open('books.json', 'r', encoding='utf-8') as file:
                self.books = json.load(file)
        except FileNotFoundError:
            self.books = []

    def load_users(self):
        try:
            with open('users.json', 'r', encoding='utf-8') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            self.users = []

    def get_book(self, book_id):
        return next((book for book in self.books if book['book_id'] == book_id), None)

    def get_book_by_title(self, title):
        return next((book for book in self.books if book['title'] == title), None)

    def get_user(self, user_id):
        return next((user for user in self.users if user['user_id'] == user_id), None)

    def main_menu(self):
        while True:
            print("\n1. Show available books\n2. Show user information\n3. Borrow a book\n4. Return a book\n5. Quit\n6.Rbooks\n7.Rusers")
            option = input("Select an option: ")
            if option == "1":
                self.show_available_books()
            elif option == "2":
                users = self.show_users()
                while True:
                    user_id = int(input("Select user: "))
                    if user_id <= len(users):
                        break
                user = self.get_user(user_id)
                if user:
                    print(f"\nFirst Name: {user['first_name']}\nLast Name: {user['last_name']}\nDebt: {user['debt']}\n")
                    while True:
                        dec = input("Do you want to pay the debt? (y/n): ").lower()
                        if dec == "y":
                            debt = int(input("Enter amount to pay: "))
                            self.del_user_debt(user_id, debt)
                            break
                        elif dec == "n":
                            break
                        else:
                            print("Invalid option")
            elif option == "3":
                self.borrow_book()
            elif option == "4":
                self.return_book()
            elif option == "6":
                self.restart_books_data()
            elif option == "7":
                self.restart_user_data()
            elif option.lower() == "quit" or option == "5":
                print("Exiting program.")
                break
            else:
                print("Invalid option. Please select again.")


if __name__ == "__main__":
    library = Library()
    library.main_menu()