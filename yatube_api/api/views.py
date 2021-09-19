from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user)


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Из условий задания я понял, что нужно настроить поиск лишь по подпискам,
    а не по подписчикам. Если добавить в search_fields параметр
    'user__username', тогда нужно переписать метод get_queryset,
    так, как в текущей его версии мы получаем в список лишь подписки
    пользователя совершившего запрос. При такой постановке задачи,
    я бы сделал так:

    def get_queryset(self):
        user = self.request.user
        if self.request.GET == {}: # проверяем, что поиск пуст
            return user.following.all()
        return Follow.objects.all()

    Тестам это все не нравится, поэтому пишу тут.
    """
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=following__username',)

    def get_queryset(self):
        user = self.request.user
        return user.following.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
