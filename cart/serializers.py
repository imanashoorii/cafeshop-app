from rest_framework import serializers
from .models import Order, OrderItem
from .utils import toJalaliDateTime


class JalaliDateTimeField(serializers.Field):
    def to_representation(self, value):
        return toJalaliDateTime(value, time=True)

    def to_internal_value(self, data):
        return


class OrderSerializer(serializers.ModelSerializer):
    createdAt = JalaliDateTimeField()
    orderedAt = JalaliDateTimeField()

    class Meta:
        model = Order
        fields = "__all__"
