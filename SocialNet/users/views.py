import logging

from django.contrib.auth.models import User

from rest_framework import generics, permissions


from .serializers import UserSerializer
from .permissions import IsSelfOrReadOnly

logger = logging.getLogger(__name__)


class UserCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class UserRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSelfOrReadOnly]
    model = User
