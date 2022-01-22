from django.urls import path
from menu.views import CreateMenuItem

urlpatterns = [
    path("menu/create", CreateMenuItem.as_view())
]
