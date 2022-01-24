from django.urls import path
from menu.views import CreateMenuItem, ListMenuCategories, CreateMenuCategory, DeleteMenuCategory

urlpatterns = [
    path("menu/create", CreateMenuItem.as_view()),
    path("menu/category/list", ListMenuCategories.as_view()),
    path('menu/category/create', CreateMenuCategory.as_view()),
    path('menu/category/<int:pk>/delete', DeleteMenuCategory.as_view())
]
