import csv
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Q

from .models import Book, Genre, BookReadHistory
import os

def export_books(request):
    return render(request, 'export_books.html')

def export_books_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Author', 'Publication Date'])
    books = Book.objects.all().values_list('title', 'author', 'publication_date')
    for book in books:
        writer.writerow(book)
    return response

def export_books_pdf(request):
    books = Book.objects.all()
    template_path = 'book_list.html'
    context = {'books': books}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="books.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def book_list(request):
    genre_id = request.GET.get('genre')
    query = request.GET.get('q', '')
    genres = Genre.objects.all()
    books = Book.objects.all()
    if genre_id:
        books = books.filter(genre_id=genre_id)
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query)
        )
    return render(request, 'books/book_list.html', {
        'books': books,
        'genres': genres,
        'selected_genre': int(genre_id) if genre_id else None,
    })
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    docx_content = None
    is_pdf = False
    is_docx = False
    if book.file:
        name = book.file.name.lower()
        is_pdf = name.endswith('.pdf')
        is_docx = name.endswith('.docx')
        if is_docx:
            try:
                from docx import Document
                doc_path = book.file.path
                document = Document(doc_path)
                docx_content = '\n'.join([para.text for para in document.paragraphs if para.text.strip()])
                if not docx_content:
                    docx_content = "Không có nội dung trong file Word."
            except Exception as e:
                docx_content = f"Lỗi khi đọc file Word: {e}"
    if request.user.is_authenticated:
        BookReadHistory.objects.get_or_create(user=request.user, book=book)
    read_histories = book.read_histories.select_related('user').order_by('-read_at')
    return render(request, 'books/book_detail.html', {
        'book': book,
        'docx_content': docx_content,
        'is_pdf': is_pdf,
        'is_docx': is_docx,
        'read_histories': read_histories,
    })
    
    if request.user.is_authenticated:
        BookReadHistory.objects.get_or_create(user=request.user, book=book)

    
    read_histories = book.read_histories.select_related('user').order_by('-read_at')

    return render(request, 'books/book_detail.html', {
        'book': book,
        'docx_content': docx_content,
        'read_histories': read_histories,
    })

from django.contrib.auth.decorators import login_required

@login_required
def read_history(request):
    histories = BookReadHistory.objects.filter(user=request.user).select_related('book').order_by('-read_at')
    return render(request, 'books/read_history.html', {
        'histories': histories,
    })
def book_list(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    genre_id = request.GET.get('genre')  # <-- thêm dòng này
    if genre_id:
        books = books.filter(genre_id=genre_id)
    q = request.GET.get('q')
    if q:
        books = books.filter(title__icontains=q)
    return render(request, 'books/book_list.html', {
        'books': books,
        'genres': genres,
        'selected_genre': int(genre_id) if genre_id else None,
    })