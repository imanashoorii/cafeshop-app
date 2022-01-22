from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Menu
from .serializers import MenuSerializer


class CreateMenuItem(generics.CreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsAdminUser,
                          IsAuthenticated,)

