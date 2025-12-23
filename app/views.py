from rest_framework import viewsets, permissions
from .models import CustomUser, Group, TeamTable
from .serializers import UserSerializer, GroupSerializer, TeamTableSerializer

# CRUD для пользователей
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# CRUD для групп
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

# CRUD для задач команды
class TeamTableViewSet(viewsets.ModelViewSet):
    queryset = TeamTable.objects.all()
    serializer_class = TeamTableSerializer
    permission_classes = [permissions.IsAuthenticated]
