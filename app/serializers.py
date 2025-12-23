# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User  # если используешь стандартного User
from .models import CustomUser, Group, TeamTable  # если кастомный


# 1. Сериалайзер для пользователя
class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для стандартного User или CustomUser"""
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        # Если кастомный пользователь — меняй модель на CustomUser
        model = CustomUser  # или User
        fields = [
            'id',
            'username',         # есть у обоих
            'email',            # есть у обоих
            'name',             # только у CustomUser
            'firstname',
            'surname',
            'created',
            'full_name',
        ]
        read_only_fields = ['id', 'created', 'full_name']

    def get_full_name(self, obj):
        if hasattr(obj, 'firstname') and hasattr(obj, 'surname'):
            return f"{obj.firstname} {obj.surname}".strip()
        return obj.get_full_name()  # fallback для стандартного User


# 2. Сериалайзер для Группы (Gr)
class GroupSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),  # или User.objects.all()
        source='author',
        write_only=True
    )
    members_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = [
            'id',
            'title',
            'author',
            'author_id',
            'created',
            'description',
            'members_count',
        ]
        read_only_fields = ['id', 'created', 'members_count']

    def get_members_count(self, obj):
        # Считаем количество событий в группе (или можно добавить ManyToMany участников)
        return obj.team_events.count()


# 3. Полный сериалайзер для TeamTable (TmTb)
class TeamTableSerializer(serializers.ModelSerializer):
    member = UserSerializer(read_only=True)
    member_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),  # или User.objects.all()
        source='member',
        allow_null=True,
        required=False
    )
    group = GroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        source='group',
        allow_null=True,
        required=False,
        default=None
    )

    # Красивое отображение даты и времени
    datetime = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TeamTable
        fields = [
            'id',
            'title',
            'date',
            'time',
            'datetime',         # объединённая дата+время
            'member',
            'member_id',
            'description',
            'group',
            'group_id',
            'status',
            'is_done',
        ]
        read_only_fields = ['id', 'datetime']

    def get_datetime(self, obj):
        return f"{obj.date} {obj.time}"

    # Валидация: если is_done=True, то статус должен быть completed
    def validate(self, data):
        if data.get('is_done') and data.get('status') != 'completed':
            data['status'] = 'completed'
        elif not data.get('is_done') and data.get('status') == 'completed':
            raise serializers.ValidationError(
                "Если статус 'completed', то is_done должно быть True"
            )
        return data