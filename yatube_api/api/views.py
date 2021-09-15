from django.shortcuts import get_object_or_404
from posts.models import Comment, Follow, Group, Post
from rest_framework import permissions, viewsets, filters
from rest_framework.pagination import LimitOffsetPagination

from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, GroupSerializer,
                          FollowSerializer, PostSerializer)


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
        post_idw = self.kwargs.get("post_id")
        get_object_or_404(Post, pk=post_idw)
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following',)

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
