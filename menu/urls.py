from django.urls import path
from menu.views import CreateMenuItem,\
    ListMenuCategories,\
    CreateMenuCategory,\
    DeleteMenuCategory,\
    ListMenuItemsByCategoryId,\
    DeleteMenuItem,\
    GetMenuItemById, \
    ListAllMenuItems, \
    ListAllTypes

urlpatterns = [
    path("menu/create", CreateMenuItem.as_view()),
    path('menu/list', ListAllMenuItems.as_view()),
    path('menu/list/<int:category>/<int:type>', ListMenuItemsByCategoryId.as_view()),
    path('menu/detail/<int:pk>', GetMenuItemById.as_view()),
    path('menu/delete/<int:pk>', DeleteMenuItem.as_view()),
    path("menu/category/list", ListMenuCategories.as_view()),
    path('menu/category/create', CreateMenuCategory.as_view()),
    path('menu/category/<int:pk>/delete', DeleteMenuCategory.as_view()),
    path('menu/type', ListAllTypes.as_view())
]
