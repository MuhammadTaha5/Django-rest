from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', views.login.as_view()),
    path('users/', views.users.as_view()),
    path('users/<str:id>/', views.UserDetail.as_view())
]