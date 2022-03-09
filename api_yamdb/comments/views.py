from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Comment, Review
from .serializers import CommentSerializer, ReviewSerializer
from .permissions import IsAuthorOrReadOnlyPermission


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        review = self.kwargs.get("review_id")
        new_queryset = Comment.objects.filter(review_id=review)
        return new_queryset


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        title = self.kwargs.get("title_id")
        new_queryset = Review.objects.filter(title_id=title)
        return new_queryset
