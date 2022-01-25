from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Menu, Category, Type
from .serializers import MenuSerializer, \
    CategorySerializer, \
    ListMenuByCategorySerializer, \
    TypeSerializer


class CreateMenuItem(generics.CreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAdminUser,
                          IsAuthenticated,)


class ListAllMenuItems(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class ListMenuItemsByCategoryId(generics.ListAPIView):
    lookup_url_kwarg_category = 'category'
    lookup_url_kwarg_type = 'type'

    def get(self, request, *args, **kwargs):
        category = self.kwargs[self.lookup_url_kwarg_category]
        type = self.kwargs[self.lookup_url_kwarg_type]
        menu = Menu.objects.filter(category__name=category, type__name=type)
        serializer = ListMenuByCategorySerializer(menu, many=True)
        return Response(serializer.data)


class GetMenuItemById(generics.RetrieveAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class DeleteMenuItem(generics.DestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsAuthenticated,
                          IsAdminUser)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={"message": "deleted!"}, status=status.HTTP_204_NO_CONTENT)


class CreateMenuCategory(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,
                          IsAdminUser)


class DeleteMenuCategory(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,
                          IsAdminUser)


class ListMenuCategories(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,
                          IsAdminUser)


class ListAllTypes(generics.ListAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = (IsAuthenticated,
                          IsAdminUser)
