from rest_framework import serializers
from .models import Menu, Category, Type


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_name_display')

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
    type = serializers.StringRelatedField(many=False, read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    type_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Menu
        # exclude = ['id']
        fields = '__all__'
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
            },
            'type_id': {
                'required': True,
                "error_messages": {
                    "required": "نوع وارد نشده است",
                },
            },
        }


class ListMenuByCategorySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=False, read_only=True)
    type = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Menu
        exclude = ("id",)


class TypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_name_display')

    class Meta:
        model = Type
        fields = '__all__'
