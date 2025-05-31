from django.contrib import admin
from .models import Author, Genre, Book,  BookImage, BookReadHistory
from .models import BookReadHistory

class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'publication_date', 'available')
    list_filter = ('available', 'genre', 'author')
    inlines = [BookImageInline]

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(BookImage)
class BookImageAdmin(admin.ModelAdmin):
    list_display = ('book', 'image')
    


@admin.register(BookReadHistory)
class BookReadHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'read_at')
    list_filter = ('user', 'book')