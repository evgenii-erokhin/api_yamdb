from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
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


class Genre(models.Model):
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
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=256,
    )

    year = models.IntegerField(
        'Год выпуска',
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
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )

    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title_id', 'genre_id'),
                name='unique_genre_to_title',
            )
        ]


class Review(models.Model):
    '''Модель отзывов'''
    author = models.IntegerField()

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
                              related_name='reviews',
                              verbose_name='Отзыв произведения',
                              )
    pub_date = models.DateTimeField(verbose_name='Дата отзыва',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [models.UniqueConstraint(
            fields=['author', 'title'], name='unique_author_title'
        )]

    def __str__(self):
        return self.text[:settings.NUMBER_VISIBLE_SYMBL]


class Comment(models.Model):
    '''Модель комментариев'''
    author = models.IntegerField()
    text = models.TextField(max_length=1000,
                            verbose_name='Текст комментария',
                            help_text='Оставьте комментарий')
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Комментарий к отзыву')
    pub_date = models.DateTimeField(verbose_name='Дата комментария',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:settings.NUMBER_VISIBLE_SYMBL]
