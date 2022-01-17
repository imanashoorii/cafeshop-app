from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserRegistration, LogoutAPIView, CustomAuthToken, UserChangePassword

urlpatterns = [
    path('login/', CustomAuthToken.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('register/', UserRegistration.as_view()),
    path('change/password/<int:pk>/', UserChangePassword.as_view())
]