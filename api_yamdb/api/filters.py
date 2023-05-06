from django_filters import rest_framework as filters

from reviews.models import Category, Genre, Title


class TitleFilter(filters.FilterSet):
    category = filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        field_name='category',
        to_field_name='slug',
    )
    genre = filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(),
        field_name='genre__slug',
        to_field_name='slug',
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre',)
