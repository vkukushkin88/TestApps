import logging

from django.urls import path
from post import views


logger = logging.getLogger(__name__)


urlpatterns = [
    path('', views.PostCreateView.as_view(), name='post-create'),
    path('<int:post_id>/', views.PostRUDView.as_view(), name='post-detail'),
    path('<int:pk>/like/', views.PostLikeView.as_view(),
         name='post-like-like'),
    path('<int:pk>/unlike/', views.PostDeleteLikeView.as_view(),
         name='post-like-unlike'),
]
