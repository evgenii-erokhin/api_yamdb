from django.db.models import Avg
from django.forms.models import model_to_dict
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class HashableDict(dict):
    def __hash__(self):
        return hash(frozenset(self.items()))


class SlugInDictOutField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        return HashableDict(model_to_dict(obj, fields=('name', 'slug')))


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = SlugInDictOutField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    genre = SlugInDictOutField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = ('id', 'rating')

    def get_rating(self, obj):
        if obj.reviews.exists():
            return round(obj.reviews.aggregate(Avg('score'))['score__avg'])
        return None


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = (
            'id', 'author', 'text', 'pub_date'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = (
            'id', 'author', 'text', 'score', 'pub_date'
        )

    def validate(self, data):

        if self.context.get('request').method != 'POST':
            return data
        reviewer = self.context.get('request').user.id
        title_id = self.context.get('view').kwargs['title_id']
        if Review.objects.filter(author=reviewer, title__id=title_id).exists():
            raise serializers.ValidationError(
                'Оставлять отзыв на одно произведение дважды запрещено!'
            )
        return data
