from rest_framework.serializers import ModelSerializer, ValidationError, ReadOnlyField
from .models import Post, Category, Tag
from django.db.models import Avg
from review.serializers import CommentsSerializer
from review.models import Comment

class ValidationMixin:

    def validate_title(self, title):
        if self.Meta.model.objects.filter(title=title).exists():
            raise ValidationError('Такое название уже существует')
        return title


class CategorySerializer(ValidationMixin, ModelSerializer):

    class Meta:
        model = Category
        fields = ('title',)

    def validate_title(self, title):
        if self.Meta.model.objects.filter(title=title).exists():
            raise ValidationError('Такое название уже существует')
        return title

class TagSerializer(ValidationMixin, ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ('title',)


class PostDetailSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.name')

    class Meta:
        model = Post
        fields = '__all__'


    def create(self, validated_data):
        user = self.context.get('request').user
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(author=user, **validated_data)
        post.tags.add(*tags)
        return post
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ratings'] = instance.ratings.aggregate(Avg('rating'))
        ['rating__avg']
        representation['comments'] = CommentsSerializer(Comment.objects.filter(post=instance.pk), many=True).data
        return representation


class PostListSerializer(ValidationMixin,ModelSerializer):

    class Meta:
        model = Post
        fields = ['author', 'title', 'body']

