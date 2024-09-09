

# Create your views here.
# library/views.py

from django.shortcuts import render, redirect
from .json_storage import Library
from django.http import Http404

# Initialize the library
library = Library()

def index(request):
    """ Show available books """
    context = {'books': library.books}
    return render(request, 'library/index.html', context)

def user_list(request):
    """ Show user information """
    context = {'users': library.users}
    return render(request, 'library/users.html', context)

def borrow_book(request):
    """ Borrow a book """
    if request.method == 'POST':
        user_id = int(request.POST.get('user_id'))
        book_id = int(request.POST.get('book_id'))

        found_book = library.get_book(book_id)
        if found_book and not found_book["borrowed"]:
            library.add_books_to_user(user_id, found_book["title"])
            library.set_book_borrowed(book_id)
            return redirect('index')
        else:
            context = {'error': "Book not available"}
            return render(request, 'library/borrow_book.html', context)

    context = {'users': library.users, 'books': library.books}
    return render(request, 'library/borrow_book.html', context)

def return_book(request):
    """ Return a book """
    if request.method == 'POST':
        user_id = int(request.POST.get('user_id'))
        book_id = int(request.POST.get('book_id'))
        user = library.get_user(user_id)
        if user and book_id:
            borrow_date = request.POST.get('borrow_date')
            return_date = request.POST.get('return_date')
            months = library.calculate_months(borrow_date, return_date)
            debt = 5 + 5 * (months - 2) if months > 2 else 5
            library.add_user_debt(user_id, debt)
            library.set_book_unborrowed_title(user["books"][book_id - 1])
            library.del_book_to_user(user_id, book_id)
            return redirect('user_list')

    context = {'users': library.users}
    return render(request, 'library/return_book.html', context)

def book_detail(request, book_id):
    try:
        book = library.get_book2(book_id)
    except Http404:
        return render(request, '404.html', status=404)

    return render(request, 'library/book_detail.html', {'book': book})