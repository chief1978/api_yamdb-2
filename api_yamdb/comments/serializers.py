from rest_framework import serializers

from .models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title_id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug'
    )

    def validate(self, data):
        if data['score'] not in range(1, 11):
            raise serializers.ValidationError(
                "Оценка должна быть в диапазоне [1, 10]"
            )
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review_id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Comment
