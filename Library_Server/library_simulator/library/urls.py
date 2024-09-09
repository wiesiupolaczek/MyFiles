# library/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.user_list, name='user_list'),
    path('borrow_book/', views.borrow_book, name='borrow_book'),
    path('return_book/', views.return_book, name='return_book'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),  # New URL pattern
]