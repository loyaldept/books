# books/urls.py - #@completed by Zuhayr Abdullazhanov
from django.urls import path
from .views import home, book_list
urlpatterns = [
    path('', home, name='home'),  # Root URL for the home page
    path('books/', book_list, name='book_list'),  # URL for viewing the book list
]
