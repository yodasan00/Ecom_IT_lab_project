from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("book_name", "author_name", "price", "created_at")
    search_fields = ("book_name", "author_name")
    list_filter = ("author_name",)
    ordering = ("book_name",)
