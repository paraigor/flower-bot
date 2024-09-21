from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    id_tg = models.IntegerField(
        "id в телеграмм", blank=True, null=True, unique=True
    )
    full_name = models.CharField("ФИО", max_length=200)
    phone_number = PhoneNumberField("Номер телефона", null=True, region="RU")

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Motive(models.Model):
    title = models.CharField("Повод", max_length=200)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Повод"
        verbose_name_plural = "Поводы"


class Budget(models.Model):
    title = models.CharField("Название", max_length=200)
    value_from = models.FloatField("Сумма от")
    value_to = models.FloatField("Сумма до")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Бюджет"
        verbose_name_plural = "Бюджеты"


class BunchElement(models.Model):
    title = models.CharField("Название элемента букета", max_length=200)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Элемент букета"
        verbose_name_plural = "Элементы букета"


class Bunch(models.Model):
    title = models.CharField("Название букета", max_length=200)
    price = models.FloatField("Цена букета")
    image = models.ImageField("Изображение букета", null=True, blank=True)
    caption = models.TextField("Описание букета", null=True, blank=True)
    motive = models.ManyToManyField(
        Motive,
        related_name="bunch",
        verbose_name="Повод",
    )
    elements = models.ManyToManyField(
        BunchElement,
        through="BunchAssembly",
        related_name="bunch",
        verbose_name="Элементы букета",
    )

    def __str__(self) -> str:
        return f"Букет / {self.price} / {self.id}"

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"


class BunchAssembly(models.Model):
    bunch = models.ForeignKey(
        Bunch, on_delete=models.PROTECT, verbose_name="Букет"
    )
    element = models.ForeignKey(
        BunchElement, on_delete=models.PROTECT, verbose_name="Элемент букета"
    )
    quantity = models.IntegerField("Количество", default=1)

    def __str__(self) -> str:
        return f"{self.bunch} / {self.element} / {self.quantity}"

    class Meta:
        verbose_name = "Элемент букета"
        verbose_name_plural = "Элементы букета"


class Order(models.Model):
    STATUSES = [
        ("accepted", "Принят"),
        ("confirmed", "Подтвержден"),
        ("completed", "Выполнен"),
        ("canceled", "Отменен"),
    ]
    status = models.CharField(
        "Статус заказа", max_length=9, choices=STATUSES, default="accepted"
    )
    date = models.DateField("Дата заказа", auto_now_add=True)
    time = models.TimeField("Время заказа", auto_now_add=True)
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, verbose_name="Клиент"
    )
    bunch = models.ForeignKey(
        Bunch, on_delete=models.PROTECT, verbose_name="Букет"
    )
    delivery_date = models.DateField("Дата доставки")
    delivery_time = models.TimeField("Время доставки")
    delivery_address = models.TextField(
        verbose_name="Адрес доставки", max_length=200, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.status} {self.date} {self.client.full_name}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
