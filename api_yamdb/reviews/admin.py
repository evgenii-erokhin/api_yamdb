from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'text',
        'score',
        'pub_date',
        'title'
    )
    list_editable = ('text',)
    search_fields = ('text',)
    list_filter = ('pub_date',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'text',
        'review',
        'pub_date',
    )
    list_editable = ('text',)
    search_fields = ('text',)
    list_filter = ('pub_date',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    list_editable = ('description', 'category')
    search_fields = ('name',)
    list_filter = ('year',)


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
