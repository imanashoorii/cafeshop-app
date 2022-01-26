from django.urls import path
from .views import OrderSummaryAdmin, OrderSummaryUser

urlpatterns = [
    path('admin/orders/list', OrderSummaryAdmin.as_view()),
    path('owner/orders/list', OrderSummaryUser.as_view())
]
