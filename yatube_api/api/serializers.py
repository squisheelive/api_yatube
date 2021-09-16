from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('__all__')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    queryset = User.objects.all()
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=queryset
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def create(self, validated_data):
        user = validated_data['user']
        following = validated_data['following']
        if user == following:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        elif Follow.objects.filter(user=user, following=following):
            raise serializers.ValidationError(
                'Такая подписка уже существует!'
            )
        follow = Follow(user=user, following=following)
        follow.save()
        return follow
