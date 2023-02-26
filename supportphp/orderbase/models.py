from django.db import models


class Client(models.Model):
    telegram_id = models.CharField(
        'ID',
        unique=True,
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
        return f'{self.name} - подписка активна:{self.subscription_is_active}'


class Maker(models.Model):
    telegram_id = models.CharField(
        'ID',
        unique=True,
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
        return f'{self.name} - подписка активна:{self.subscription_is_active}'


class Order(models.Model):
    order_datetime = models.DateTimeField(
        'Дата и время формирования заявки ',
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
        return f'{self.name} заказчик: {self.client} - исполнитель: {self.maker} - выполнено: {self.order_is_done}'


class Conversation(models.Model):
    message_datetime = models.DateTimeField(
        'Дата и время отправки сообщения',
        auto_now=True,
        null=False,
        blank=False,
    )
    order_id = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        null=True,
        blank=True,
    )
    message_sender = models.CharField(
        'Отправитель сообщения (ID)',
        max_length=200,
    )
    message_receiver = models.CharField(
        'Получатель сообщения (ID)',
        max_length=200,
    )
    message_text = models.TextField(
        'Текст сообщения',
    )
    message_is_read = models.BooleanField(
        'Сообщение прочитано',
    )

    def __str__(self):
        return f'{self.message_datetime} ' \
               f'from:{self.message_sender} ' \
               f'to:{self.message_receiver} - ' \
               f'is read:{self.message_is_read}'
