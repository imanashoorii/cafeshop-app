import re
from datetime import datetime

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
        user.updatedAt = datetime.now()
        user.save()
        return user

