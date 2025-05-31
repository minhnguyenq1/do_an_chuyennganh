from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('books/', views.book_list, name='book_list'),
    path('<int:pk>/', views.book_detail, name='book_detail'),
    path('export_books/', views.export_books, name='export_books'),
    path('books/export/csv/', views.export_books_csv, name='export_books_csv'),
    path('books/export/pdf/', views.export_books_pdf, name='export_books_pdf'),
    path('read-history/', views.read_history, name='read_history'),
    
]