from rest_framework.serializers import ModelSerializer, ValidationError, ReadOnlyField
from.models import Comment, Like, Rating

class CommentsSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.name')

    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.name')

    class Meta:
        model = Rating
        fields = '__all__'


    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        rating = Rating.objects.create(author=user, **validated_data)
        return rating
    
    def validate_rating(self, rating):
        if not 0 <= rating <= 10:
            raise ValidationError('Рейтинг должен быть от 0 до 10')
        return rating

    
    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)
    
    