from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from users.permissions import UserIsOwnerOrReadOnly
from .models import Order, OrderItem
from .serializers import OrderSerializer
from django.http import Http404


class OrderSummaryAdmin(generics.ListAPIView):
    queryset = Order.objects.all().order_by("user")
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,
                          IsAdminUser)


class OrderSummaryUser(APIView):
    permission_classes = (IsAuthenticated,
                          UserIsOwnerOrReadOnly,)

    def get_object(self, pk, mode):
        if mode == 'all':
            return Order.objects.filter(user=pk)
        return Order.objects.filter(user=pk, ordered=False)

    def get(self, request):
        userId = request.user.id
        mode = request.GET.get("mode")
        order = self.get_object(userId, mode)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


