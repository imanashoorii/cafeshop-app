import re
from datetime import datetime

from django.contrib.auth.password_validation import validate_password
from django.utils.crypto import get_random_string

from rest_framework import serializers
from .models import User


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
            raise serializers.ValidationError("شماره همراه وارد شده معتبر نیست!")
        return mobile

    def validate_email(self, email):
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(pattern, email):
            raise serializers.ValidationError("آدرس ایمیل معتبر نیست")
        return email

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
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
