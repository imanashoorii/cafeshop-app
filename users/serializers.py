import re
from datetime import datetime

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def validate_phone(self, phone):
        pattern = r'^09\d{9}$'
        if not re.match(pattern, phone):
            raise serializers.ValidationError("شماره همراه وارد شده معتبر نیست")
        return phone

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.updatedAt = datetime.now()
        user.save()
        return user

