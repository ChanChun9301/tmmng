from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, User  # выбирай один
from django.utils import timezone


# Вариант 1: Если хочешь кастомного пользователя
class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, blank=True, verbose_name="Имя (необязательно)")
    firstname = models.CharField(max_length=100, verbose_name="Имя")
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    created = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.firstname} {self.surname} ({self.username})"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


# Вариант 2: Если используешь стандартного User, то эту модель не создавай,
# а в настройках проекта укажи AUTH_USER_MODEL = 'auth.User'


class Group(models.Model):
    """Группа (Gr)"""
    title = models.CharField(max_length=200, verbose_name="Название группы")
    author = models.ForeignKey(
        # Если кастомный пользователь — CustomUser, если стандартный — 'auth.User'
        'CustomUser',  # или settings.AUTH_USER_MODEL
        on_delete=models.CASCADE,
        related_name='created_groups',
        verbose_name="Автор"
    )
    created = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class TeamTable(models.Model):
    """Элемент расписания/задачи команды (TmTb)"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    member = models.ForeignKey(
        'CustomUser',  # или settings.AUTH_USER_MODEL
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_events',
        verbose_name="Участник"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name='team_events',
        verbose_name="Группа"
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ('planned', 'Запланировано'),
            ('in_progress', 'В процессе'),
            ('completed', 'Завершено'),
            ('cancelled', 'Отменено'),
        ],
        default='planned',
        verbose_name="Статус"
    )
    is_done = models.BooleanField(default=False, verbose_name="Выполнено")

    def __str__(self):
        return f"{self.title} — {self.date} {self.time}"

    class Meta:
        verbose_name = "Элемент расписания команды"
        verbose_name_plural = "Расписание команды"
        ordering = ['date', 'time']