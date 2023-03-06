from django.db import models
import string
import random


class Profile(models.Model):
    user_id = models.CharField(max_length=50, verbose_name='Айди пользователя')
    first_name = models.CharField(max_length=100, verbose_name='Имя', null=True, blank=True)
    user_name = models.CharField(max_length=50, verbose_name='Имя пользователя')
    role = models.CharField(max_length=200, default='', verbose_name='Роль пользователя')


    def __str__(self) -> str:
        return self.first_name
    

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'


class Products(models.Model):
    product = models.CharField(max_length=1000, verbose_name='Тавар')
    count = models.ImageField(verbose_name='Колличество')
    opt_price = models.PositiveIntegerField(verbose_name="Оптовая цена")
    avalability = models.BooleanField(verbose_name='Наличие')
    photo = models.CharField(max_length=3000, verbose_name='Фото', blank=True, null=True)
    product_percent = models.FloatField(verbose_name='2.5% от суммы товара', blank=True, null=True)
    product_sum = models.PositiveIntegerField(verbose_name="Сумма товара", blank=True, null=True)
    fake_count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.product
    
    class Meta:
        verbose_name ="Товар"
        verbose_name_plural = "Товары"

class Applications(models.Model):

    CHOICES = (
        ("Ожидает упаковки", "Ожидает упаковки"),
        ("Отменен", "Отменен"),
        ("Ожидает отправки", "Ожидает отправки"),
        ("Передан логисту", "Передан логисту"),
        ("Упакован", "Упакован"),
        ("Передан диспетчеру", "Передан диспетчеру"),
        ("Доставлен", "Доставлен"),
        ("Фабричный брак", "Фабричный брак"),
        ("Дорожный брак", "Дорожный брак"),
        ("Ожидание подтверждения", "Ожидание подтверждения"),
        ("В дороге", "В дороге")
    )

    note = models.CharField(max_length=5000, verbose_name="Примечяние")
    adress = models.CharField(max_length=5000, verbose_name='Адрес')
    product = models.CharField(max_length=5000, verbose_name="Товар", blank=True, null=True)
    checks_document = models.CharField(max_length=1000, verbose_name="Чек", blank=True, null=True)
    direction = models.CharField(max_length=400, verbose_name="Направление", ull=True, blank=True)
    delivery_information = models.CharField(max_length=1000, verbose_name="Информация о доставке", blank=True, null=True)
    canceled_reason = models.CharField(max_length=3000,verbose_name="Причина отмены", blank=True, null=True)
    bool_status = models.BooleanField(verbose_name="Подт / Отм", null=True, blank=True)
    create_time = models.DateField(auto_now_add=True, verbose_name='Время создания')
    driver = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name='Водитель', related_name='drive_user', null=True, blank=True)
    status = models.CharField(max_length=200, blank=True, null=True, default='Ожидания подтверждения', choices=CHOICES, verbose_name='Статус')
    location = models.CharField(max_length=3000, verbose_name='Локация', blank=True, null=True)
    location_time = models.CharField(max_length=3000, verbose_name='Время локации', null=True, blank=True)
    time_update_location = models.DateTimeField(auto_now=True, verbose_name="Время изменнеия локации")

    user = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name="Добавил")
    products = models.ManyToManyField(Products, verbose_name="Привязанный продукт", null=True, blank=True)
    bool_count = models.BooleanField(default=True, verbose_name='Хватает ли колличество', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.driver} | {self.product} | {self.user}'
    
    class Meta:
        verbose_name ="Заявка"
        verbose_name_plural = "Заявки"

class RoleCode(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='create_user', verbose_name='Пользователь который создал код')
    active_user = models.ForeignKey(Profile, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Пользователь который активировал код')
    code = models.CharField(max_length=200, verbose_name='Код')
    role = models.CharField(max_length=200, verbose_name="Роль которая выдается после активации кода")

    def __str__(self) -> str:
        return f'{self.user} | {self.code} | {self.role}'
    

    class Meta:
        verbose_name = 'Код'
        verbose_name_plural = "Коды"
    

