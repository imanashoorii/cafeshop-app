from datetime import datetime
from django.core.cache import cache

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .kavenegar import sendLoginSMS
from .models import User, OTP
from .permissions import UserIsOwnerOrReadOnly
from .utils import otp_generator

from .serializers import UserSerializer, ChangePasswordSerializer, UpdateUserSerializer, AuthWithPhoneSerializer, \
    OTPSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user.last_login = timezone.now()
        user.save()
        return Response({
            'token': token.key,
            'message': "success",
            'userId': user.pk,
        })


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            data={'message': "user logged out"},
            status=status.HTTP_204_NO_CONTENT
        )


class UserRegistration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserChangePassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        result = {
            "message": "success",
            "status": 200,
        }
        return Response(result)


class UpdateUserProfile(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,
                          UserIsOwnerOrReadOnly,)
    serializer_class = UpdateUserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        result = {
            "message": "success",
            "details": serializer.data,
            "status": status.HTTP_200_OK,

        }
        return Response(result)


class LoginWithPhoneView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, format=None):
        serializer = AuthWithPhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get("phone")
            isUser: bool = get_user_model().objects.filter(mobile=phone).values("mobile").exists()
            if not isUser:
                return Response(
                    {"message": "کاربری با این شماره یافت نشد"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            code = otp_generator()
            otp, _ = OTP.objects.get_or_create(
                phone=phone
            )
            otp.otp = code
            otp.count = 1
            otp.save(update_fields=['otp', 'count'])
            cache.set(phone, code, 100)
            sendLoginSMS(receptor=phone, otp=code)
            context = {
                "message": "کد با موفقیت ارسال شد",
            }
            return Response(
                context,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyOTPView(APIView):
    permission_classes = [
        AllowAny,
    ]
    confirm_for_authentication = False

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            received_code = serializer.validated_data.get("code")
            otp = OTP.objects.filter(otp=received_code)

            if not otp.exists():
                return Response(
                    {
                        "message": "کد ارسال شده صحیح نمی باشد",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

            obj = otp.first()
            code_in_cache = cache.get(obj.phone)
            if code_in_cache is not None:
                if obj.otp == received_code:
                    user = get_user_model().objects.get(mobile=obj.phone)
                    self.confirm_for_authentication = True
                    if self.confirm_for_authentication:
                        token, created = Token.objects.get_or_create(user=user)
                        user.last_login = datetime.now()
                        user.save()
                        obj.delete()
                        cache.delete(obj.phone)
                        return Response({
                            'token': token.key,
                            'message': "success",
                            'userId': user.pk,
                        })
                else:
                    return Response(
                        {
                            "message": "کد ارسال شده صحیح نمی باشد",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                obj.delete()
                return Response(
                    {
                        "message": "کد ارسال شده منقضی شده است",
                    },
                    status=status.HTTP_408_REQUEST_TIMEOUT,
                )

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
