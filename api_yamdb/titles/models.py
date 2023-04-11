from django.db import models


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=50,
        unique=True,
    )

    slug = models.SlugField(
        'Слаг категории',
        unique=True,
    )


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=200,
    )

    year = models.IntegerField(
        'Год выпуска',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория произведения',
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=50,
        unique=True,
    )

    slug = models.SlugField(
        'Слаг жанра',
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class GenreTitle:
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genres',
    )

    genre_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title_id', 'genre_id'),
                name='unique_genre_to_title',
            )
        ]
