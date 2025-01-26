from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from posts.models import Comment, Post, Follow, Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'description']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'pub_date', 'image', 'group']
        read_only_fields = ['id', 'pub_date', 'author']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['group'] = instance.group.id if hasattr(
            instance, 'group'
        ) and instance.group else None
        return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ['id', 'author', 'post', 'text', 'created']
        read_only_fields = ['author', 'post']
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    following = serializers.CharField(required=True)

    class Meta:
        model = Follow
        fields = ['user', 'following']
        # Добавляем UniqueTogetherValidator для проверки уникальности
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message="Вы уже подписаны на этого пользователя."
            )
        ]

    def validate_following(self, value):
        # Проверяем, что пользователь не подписывается на себя
        if value == self.context['request'].user.username:
            raise serializers.ValidationError("Вы не можете подписаться на себя.")
        return value
