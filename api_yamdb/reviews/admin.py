from django.contrib import admin
from .models import Title, Category, Review, Comment, Genre

admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Genre)
