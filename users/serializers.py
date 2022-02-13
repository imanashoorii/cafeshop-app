import re
from django.contrib.auth.password_validation import validate_password
from django.utils.crypto import get_random_string

from rest_framework import serializers
from .models import User, OTP


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "username": {
                "error_messages": {
                    "required": "نام کاربری وارد نشده است",
                },
            },
            "password": {
                "error_messages": {
                    "required": "رمزعبور وارد نشده است",
                },
            },
            "email": {
                "error_messages": {
                    "required": "آدرس ایمیل وارد نشده است",
                },
            },
            "mobile": {
                "error_messages": {
                    "required": "شماره همراه وارد نشده است",
                },
            },
            "phone": {
                "error_messages": {
                    "required": "شماره تلفن وارد نشده است",
                },
            },
        }

    def validate_username(self, username):
        pattern = r"^[A-Za-z]+(?:[_-]*[A-Za-z0-9]+)*$"
        if not re.match(pattern, username) or "admin" in username:
            raise serializers.ValidationError("نام کاربر معتبر نمی باشد")
        return username

    def validate_mobile(self, mobile):
        pattern = r'^09\d{9}$'
        if not re.match(pattern, mobile):
            raise serializers.ValidationError("شماره همراه وارد شده معتبر نمی باشد")
        return mobile

    def validate_email(self, email):
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=email).exists():
            raise serializers.ValidationError({"error": "ایمیل تکراری است"})
        if not re.match(pattern, email):
            raise serializers.ValidationError("آدرس ایمیل معتبر نمی باشد")
        return email

    def create(self, validated_data):
        user = super().create(validated_data)
        user.refCode = get_random_string(10)
        user.save()
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attr):
        if attr.get("password") != attr.get("password2"):
            raise serializers.ValidationError({"error": "رمزعبور تطابق ندارد"})
        return attr

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError({"error": "رمزعبور پیشین صحیح نمی باشد"})
        return old_password

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'address', 'postalCode', 'email', 'mobile', 'phone')
        extra_kwargs = {
            'first_name': {
                'required': True,
                "error_messages": {
                    "required": "نام وارد نشده است",
                },
            },
            'last_name': {
                'required': True,
                "error_messages": {
                    "required": "نام خانوادگی وارد نشده است",
                },
            },
            'address': {
                'required': True,
                "error_messages": {
                    "required": "آدرس وارد نشده است",
                },
            },
            'postalCode': {
                'required': True,
                "error_messages": {
                    "required": "کدپستی وارد نشده است",
                },
            },
            "email": {
                'required': False,
            },
            "mobile": {
                'required': False,
            },
            "phone": {
                'required': False,
            },
        }

    def validate_postalCode(self, postalCode):
        user = self.context['request'].user
        pattern = r"^\b(?!(\d)\1{3})[13-9]{4}[1346-9][013-9]{5}\b$"
        if User.objects.exclude(pk=user.pk).filter(postalCode=postalCode).exists():
            raise serializers.ValidationError({"error": "کدپستی در سیستم وجود دارد"})
        if not re.match(pattern, postalCode):
            raise serializers.ValidationError({"error": "کدپستی وارد شده صحیح نمی باشد"})
        return postalCode

    def validate_mobile(self, mobile):
        pattern = r'^09\d{9}$'
        if not re.match(pattern, mobile):
            raise serializers.ValidationError("شماره همراه وارد شده معتبر نیست!")
        return mobile

    def validate_email(self, email):
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=email).exists():
            raise serializers.ValidationError({"error": "ایمیل تکراری است"})
        if not re.match(pattern, email):
            raise serializers.ValidationError("آدرس ایمیل معتبر نیست")
        return email

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.address = validated_data['address']
        instance.postalCode = validated_data['postalCode']
        instance.mobile = validated_data.get('mobile') if validated_data.get('mobile') else instance.mobile
        instance.phone = validated_data.get('phone') if validated_data.get('phone') else instance.phone
        instance.email = validated_data.get('email') if validated_data.get('email') else instance.email

        instance.save()
        return instance


class AuthWithPhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = OTP
        exclude = ["id"]
        extra_kwargs = {
            'phone': {
                'required': True,
                "error_messages": {
                    "required": "شماره موبایل وارد نشده است",
                },
            },
            'otp': {
                'required': False,
            }
        }

    def validate_phone(self, phone):
        pattern = r'^09\d{9}$'
        if not re.match(pattern, phone):
            raise serializers.ValidationError({"message": "شماره همراه وارد شده معتبر نمی باشد"})
        return phone


class OTPSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=6,
    )

    def validate_code(self, code):
        from string import ascii_letters as char
        for _ in code:
            if _ in char:
                raise serializers.ValidationError({
                    "message": "کد ارسال شده معتبر نمی باشد"
                })
        return code
