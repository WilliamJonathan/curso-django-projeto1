from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    author = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='autor')
    bio = models.TextField(default='', blank=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
