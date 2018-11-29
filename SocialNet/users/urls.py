from django.urls import path
from users import views
from rest_framework_jwt.views import (
    refresh_jwt_token, verify_jwt_token, obtain_jwt_token)


urlpatterns = [
    path('auth/api-token-auth/', obtain_jwt_token),
    path('auth/api-token-refresh/', refresh_jwt_token),
    path('auth/api-token-verify/', verify_jwt_token),

    path('', views.UserCreateView.as_view(), name='user-create'),
    path('<int:user_id>/', views.UserRUDView.as_view(), name='user-detail'),

]
