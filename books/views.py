# books/views.py - @completed by Zuhayr Abdullazhanov
from django.shortcuts import render
from .models import Book  # Assuming you have a Book model
def home(request):
    # This view renders the home.html template
    return render(request, 'books/home.html')

def book_list(request):
    # This view fetches data from the Book model and passes it to the book-list.html template
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})
