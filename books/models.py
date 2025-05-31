from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True)
    publication_date = models.DateField()
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)  # ảnh bìa
    file = models.FileField(upload_to='book_files/', null=True, blank=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='pages')
    image = models.ImageField(upload_to='book_pages/')

    def __str__(self):
        return f"Page of {self.book.title}"


from django.contrib.auth.models import User

class BookReadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='read_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='read_histories')
    read_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} đã đọc {self.book.title} lúc {self.read_at}"

   