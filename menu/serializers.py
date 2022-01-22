from rest_framework import serializers
from .models import Menu


class MenuSerializer(serializers.ModelSerializer):
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
            'category': {
                'required': True,
                "error_messages": {
                    "required": "دسته بندی وارد نشده است",
                },
            }
        }
