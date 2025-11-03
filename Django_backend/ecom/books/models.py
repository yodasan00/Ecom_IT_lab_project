from django.db import models

class Book(models.Model):
    author_name = models.CharField(max_length=255)
    book_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)  # ✅ exists
    updated_at = models.DateTimeField(auto_now=True)      # ✅ exists
