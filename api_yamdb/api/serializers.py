from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    genre = GenreSerializer(
        many=True,
    )

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        if obj.reviews.exists():
            return round(obj.reviews.aggregate(Avg('score')))
        return None

    def validate_category(self, data):
        if not Category.objects.filter(slug=data['category']).exists():
            raise serializers.ValidationError(
                {"category": "Такая категория не существует."}
            )
        return data

    def validate_genre(self, data):
        for genre in data['genre']:
            if not Genre.objects.filter(slug=genre).exists():
                raise serializers.ValidationError(
                    {"genre": f"Некорректный жанр: {genre}."}
                )
        return data

    def create(self, validated_data):
        category = validated_data.pop('category')
        genres = validated_data.pop('genre')

        validated_data['category'] = Category.objects.get(slug=category)
        title = Title.objects.create(**validated_data)

        for genre in genres:
            current_genre = Genre.objects.get(slug=genre)
            GenreTitle.objects.create(
                genre_id=current_genre,
                title_id=title,
            )

        return title


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id', 'author', 'text', 'review', 'pub_date'
        )


class ReviewSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='username',
    #     default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = (
            'id', 'author', 'text', 'score', 'title', 'pub_date'
        )
