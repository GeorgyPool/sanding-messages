from django.db import models


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Электронная почта", help_text="Введите электронную почту")
    full_name = models.CharField(max_length=300, verbose_name="Введите Ф.И.О", help_text="Иванов Иван Иванович")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий", help_text="Оставьте комментарии")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"


class Messages(models.Model):
    title = models.CharField(max_length=200, verbose_name="Тема письма", help_text="Введите тему письма")
    text = models.TextField(verbose_name="Сообщение", help_text="Введите сообщение")

    class Mete:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"

    def __str__(self):
        return self.title


class Sending(models.Model):
    END = "Завершено"
    CREATE = "Создано"
    LAUNCHED = "Запущенно"

    STATUS_CHOICES = [(END, "Завершено"), (CREATE, "Создано"), (LAUNCHED, "Запущено")]

    start_time = models.TimeField(verbose_name="С какого времени доступна рассылка")
    end_time = models.TimeField(verbose_name="До какого времени доступна рассылка")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    message = models.ForeignKey(Messages, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient, related_name="getting")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class TryingSending(models.Model):
    SUCCESS = "Удачно"
    NOT_SUCCESS = "Не удачно"

    STATUS_CHOICES = [
        (SUCCESS, "Удачно"),
        (NOT_SUCCESS, "Не удачно")
    ]

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата попытки")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус попытки")
    server_response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Sending, on_delete=models.DO_NOTHING, related_name="sending", verbose_name="Рассылка")

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
