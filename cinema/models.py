from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Film(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название фильма')
    description = models.TextField(verbose_name='Описание')
    duration = models.IntegerField(verbose_name='Длительность (мин)')
    genre = models.CharField(max_length=100, verbose_name='Жанр')

    def __str__(self):
        return self.title


class Session(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name='Фильм')
    datetime = models.DateTimeField(verbose_name='Дата и время сеанса')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    seats_available = models.IntegerField(verbose_name='Доступные места')

    def __str__(self):
        return f"{self.film.title} - {self.datetime}"


class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    tickets_count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.session.film.title}"