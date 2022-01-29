from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from users.permissions import UserIsOwnerOrReadOnly
from .models import Order, OrderItem
from menu.models import Menu
from .serializers import OrderSerializer
from datetime import datetime


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


class AddToCartOrUpdateQuantity(APIView):
    permission_classes = (IsAuthenticated,
                          UserIsOwnerOrReadOnly,)

    def get_object(self, pk):
        return get_object_or_404(Menu, pk=pk)

    def post(self, request, pk):
        item = self.get_object(pk=pk)
        orderItem, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            serializer = OrderSerializer(order)
            if order.items.filter(item__pk=item.pk).exists():
                orderItem.quantity += 1
                orderItem.save()
                return Response({"message": "Cart Updated",
                                 "data": serializer.data,
                                 "total": order.get_total_price()}, status=status.HTTP_200_OK)
            else:
                order.items.add(orderItem)
                return Response({"message": "Cart Updated",
                                 "data": serializer.data,
                                 "total": order.get_total_price()}, status=status.HTTP_200_OK)

        orderedDate = datetime.now()
        order = Order.objects.create(user=request.user, orderedAt=orderedDate)
        order.items.add(orderItem)
        serializer = OrderSerializer(order)
        return Response({"message": "Item added to cart",
                         "data": serializer.data,
                         "total": order.get_total_price()}, status=status.HTTP_201_CREATED)


class RemoveFromCart(APIView):
    permission_classes = (IsAuthenticated,
                          UserIsOwnerOrReadOnly,)

    def get_object(self, pk):
        return get_object_or_404(Menu, pk=pk)

    def post(self, request, pk):
        item = self.get_object(pk=pk)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__pk=item.pk).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                order_item.delete()
                return Response({"message": "حذف شد"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "این آیتم در سبد خرید شما نیست"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "هیچ سفارشی ندارید"}, status=status.HTTP_204_NO_CONTENT)


class ReduceCartQuantity(APIView):
    permission_classes = (IsAuthenticated,
                          UserIsOwnerOrReadOnly,)

    def get_object(self, pk):
        return get_object_or_404(Menu, pk=pk)

    def post(self, request, pk):
        item = self.get_object(pk=pk)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__pk=item.pk).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                if order_item.quantity > 0:
                    order_item.quantity -= 1
                    order_item.save()
                else:
                    order_item.delete()
                return Response({"message": "Cart Updated"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "این آیتم در سبد خرید شما نیست"})
        else:
            return Response({"message": "هیچ سفارشی ندارید"}, status=status.HTTP_204_NO_CONTENT)
