from django.db import models


class Client(models.Model):
    telegram_id = models.CharField(
        'ID',
        max_length=200,
    )
    name = models.CharField(
        'Имя',
        max_length=200,
    )
    subscription_is_active = models.BooleanField(
        'Подписка активна',
    )

    def __str__(self):
        return f'{self.name}'


class Maker(models.Model):
    telegram_id = models.CharField(
        'ID',
        max_length=200,
    )
    name = models.CharField(
        'Имя',
        max_length=200,
    )
    subscription_is_active = models.BooleanField(
        'Подписка активна',
    )

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    order_datetime = models.DateTimeField(
        'Время формирования заявки ',
        auto_now=True,
        null=False,
        blank=False,
    )

    name = models.CharField(
        'Задача',
        max_length=200,
    )

    problem = models.TextField(
        'Описание задачи',
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Клиент',
        null=False,
        blank=False,
    )

    maker = models.ForeignKey(
        Maker,
        on_delete=models.CASCADE,
        verbose_name='Исполнитель',
        null=True,
        blank=True,
    )

    exec_time = models.FloatField(
        'Время выполнения (в часах)',
        null=True,
        blank=True,
    )

    order_is_done = models.BooleanField(
        'Заявка выполнена',
        auto_created=False,
    )

    def __str__(self):
        return f'{self.name}'
