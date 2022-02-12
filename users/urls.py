from django.urls import path

from .views import UserRegistration, LogoutAPIView, CustomAuthToken, UserChangePassword, UpdateUserProfile, \
    LoginWithPhoneView, VerifyOTPView

urlpatterns = [
    path('login/', CustomAuthToken.as_view()),
    path('login/phone', LoginWithPhoneView.as_view()),
    path('login/otp/verify', VerifyOTPView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('register/', UserRegistration.as_view()),
    path('change/password/<int:pk>/', UserChangePassword.as_view()),
    path('edit/<int:pk>', UpdateUserProfile.as_view())
]
