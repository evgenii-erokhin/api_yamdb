from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import year_validator
from users.models import User


class Category(models.Model):
    '''Модель категории'''
    name = models.CharField(
        'Название категории',
        max_length=256,
        unique=True,
    )

    slug = models.SlugField(
        'Слаг категории',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    '''Модель жанра'''
    name = models.CharField(
        'Название жанра',
        max_length=256,
        unique=True,
    )

    slug = models.SlugField(
        'Слаг жанра',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    '''Модель произведения'''
    name = models.CharField(
        'Название произведения',
        max_length=256,
    )

    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[year_validator],
    )

    description = models.TextField(
        'Описание',
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория произведения',
    )

    genre = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        ordering = ('year', 'name')
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    '''Модель для связи жанра и произведения'''
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'genre'),
                name='unique_genre_to_title',
            )
        ]


class Review(models.Model):
    '''Модель отзыва'''
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор отзыва')

    text = models.TextField(max_length=3000,
                            verbose_name='Текст отзыва',
                            help_text='Введите текст отзыва')

    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка произведения',
        help_text='Укажите оценку произведения',
        validators=[MinValueValidator(1, 'Оценка не может быть меньше 1-го'),
                    MaxValueValidator(10, 'Оценка не может быть боьше 10-ти')]
    )

    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              verbose_name='Отзыв произведения',
                              )
    pub_date = models.DateTimeField(verbose_name='Дата отзыва',
                                    auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [models.UniqueConstraint(
            fields=['author', 'title'], name='unique_author_title'
        )]

    def __str__(self):
        return self.text[:settings.NUMBER_VISIBLE_SYMBL]


class Comment(models.Model):
    '''Модель комментария'''
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор комментария')
    text = models.TextField(max_length=1000,
                            verbose_name='Текст комментария',
                            help_text='Оставьте комментарий')
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               verbose_name='Комментарий к отзыву')
    pub_date = models.DateTimeField(verbose_name='Дата комментария',
                                    auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:settings.NUMBER_VISIBLE_SYMBL]
