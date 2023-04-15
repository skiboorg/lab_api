import datetime
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save, pre_delete
from django.utils import timezone
from datetime import timedelta
# from .tasks import send_email

import logging
logger = logging.getLogger(__name__)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, login, password, **extra_fields):
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(login, password, **extra_fields)

    def create_superuser(self, login, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(login, password, **extra_fields)



class User(AbstractUser):
    username = None
    firstname = None
    lastname = None

    added_by = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True)
    fio = models.CharField('ФИО', max_length=50, blank=True, null=True)
    work = models.CharField('Должность', max_length=50, blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to='user/avatars')
    login = models.CharField('Логин',max_length=20, blank=True, null=True, unique=True)


    is_moderator = models.BooleanField('Локальный админ', default=False)
    comment = models.TextField('Комментарий', blank=True, null=True)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f'{self.fio} {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = '1. Пользователи'


def user_post_save(sender, instance, created, **kwargs):
    #import monthdelta
    #datetime.date.today() + monthdelta.monthdelta(months=1)

    if created:
        print('created')


post_save.connect(user_post_save, sender=User)


