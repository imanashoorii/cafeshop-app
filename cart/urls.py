from django.urls import path
from .views import OrderSummaryAdmin, OrderSummaryUser, AddToCartOrUpdateQuantity, RemoveFromCart, ReduceCartQuantity

urlpatterns = [
    path('admin/orders/list', OrderSummaryAdmin.as_view()),
    path('owner/orders/list', OrderSummaryUser.as_view()),
    path('owner/<int:pk>/add', AddToCartOrUpdateQuantity.as_view()),
    path('owner/<int:pk>/remove', RemoveFromCart.as_view()),
    path('owner/<int:pk>/reduce', ReduceCartQuantity.as_view()),
]
