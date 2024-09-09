# library/json_storage.py

import json
import os
import names
from datetime import datetime
from requests import get

class Library:
    books_file = os.path.join(os.path.dirname(__file__), 'books.json')
    users_file = os.path.join(os.path.dirname(__file__), 'users.json')

    def __init__(self):
        self.books = []
        self.users = []
        self.load_books()
        self.load_users()

    def restart_books_data(self):
        query = get("https://wolnelektury.pl/api/books/")
        self.books = [{"book_id": book_id, "title": book["title"], "borrowed": False} for book_id, book in enumerate(query.json(), start=1)]
        self.save_books()

    def save_books(self):
        with open(self.books_file, 'w', encoding='utf-8') as file:
            json.dump(self.books, file, ensure_ascii=False, indent=4)

    def restart_user_data(self):
        self.users = [{"user_id": user_id, "first_name": first_name, "last_name": last_name, "debt": 0, "books": []}
                      for user_id, (first_name, last_name) in enumerate(self.generate_names(100), start=1)]
        self.save_users()

    def save_users(self):
        with open(self.users_file, 'w', encoding='utf-8') as file:
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
            if user["debt"] < 0:
                user["debt"] = 0
            self.save_users()

    def calculate_months(self, start_date_str, end_date_str, date_format="%d-%m-%Y"):
        start_date = datetime.strptime(start_date_str, date_format)
        end_date = datetime.strptime(end_date_str, date_format)
        year_diff = end_date.year - start_date.year
        month_diff = end_date.month - start_date.month
        return year_diff * 12 + month_diff

    def load_books(self):
        try:
            with open(self.books_file, 'r', encoding='utf-8') as file:
                self.books = json.load(file)
        except FileNotFoundError:
            self.books = []

    def load_users(self):
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            self.users = []

    def get_book(self, book_id):
        return next((book for book in self.books if book['book_id'] == book_id), None)

    def get_book_by_title(self, title):
        return next((book for book in self.books if book['title'] == title), None)

    def get_user(self, user_id):
        return next((user for user in self.users if user['user_id'] == user_id), None)

    def get_book2(self, book_id):
        book = next((book for book in self.books if book['book_id'] == book_id), None)
        if not book:
            raise Http404("Book not found")
        return book