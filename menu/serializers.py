from rest_framework import serializers
from .models import Menu, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {
            'name': {
                'required': True,
                "error_messages": {
                    "required": "نام وارد نشده است",
                },
            },
        }


class MenuSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=False, read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Menu
        exclude = ['id']
        extra_kwargs = {
            'name': {
                'required': True,
                "error_messages": {
                    "required": "نام وارد نشده است",
                },
            },
            'photo': {
                'required': True,
                "error_messages": {
                    "required": "عکس آپلود نشده است",
                },
            },
            'price': {
                'required': True,
                "error_messages": {
                    "required": "قیمت وارد نشده است",
                },
            },
            'category_id': {
                'required': True,
                "error_messages": {
                    "required": "دسته بندی وارد نشده است",
                },
            }
        }


class ListMenuByCategorySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=False, read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Menu
        exclude = ("id",)
        extra_kwargs = {
            'category_id': {
                'required': True,
                "error_messages": {
                    "required": "دسته بندی وارد نشده است",
                },
            }
        }
