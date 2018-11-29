import logging
from rest_framework import generics, permissions
from rest_framework.response import Response

from post.permissions import IsAuthor, IsSelfOrReadOnly
from post.models import Post

from .serializers import PostSerializer


logger = logging.getLogger(__name__)


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSelfOrReadOnly]
    model = Post


class PostDeleteLikeView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSelfOrReadOnly]
    model = Post


class PostLikeView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request, pk):
        post = self.get_object()
        if post.user != request.user:
            post.add_once(request.user)

        return Response(self.get_serializer().data)
