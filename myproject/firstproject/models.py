from django.db import models
from django.contrib.auth.models import User

# Максимальная длина для текстовых полей
MAX_LENGTH = 255

# Старые модели (игнорируем)
class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование категориииии')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категорииииии'

    def __str__(self):
        return self.name

class Collection(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование коллекции')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'

    def __str__(self):
        return self.name

class Clothes(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование одежды')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    size = models.PositiveSmallIntegerField(default=36, verbose_name='Размер')
    color = models.CharField(max_length=MAX_LENGTH, verbose_name='Цвет')
    photo = models.ImageField(upload_to='', null=True, blank=True, verbose_name='Изображение')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    is_exists = models.BooleanField(default=True, verbose_name='Доступность к заказу')

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.PROTECT)
    collection = models.ManyToManyField(Collection, verbose_name='Коллекция')

    class Meta:
        verbose_name = 'Одежда'
        verbose_name_plural = 'Одежда'

    def __str__(self):
        return f"{self.name} - ({self.price} Рублей)"

# Новые модели (основной фокус)
class SportCategory(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование категории')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class ProductType(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Тип товара')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Типы товаров'

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование бренда')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name

class SportProduct(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование товара')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    size = models.CharField(max_length=MAX_LENGTH, null=True, blank=True, verbose_name='Размер')
    material = models.CharField(max_length=MAX_LENGTH, null=True, blank=True, verbose_name='Материал')
    stock = models.PositiveSmallIntegerField(default=0, verbose_name='Количество на складе')
    photo = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Изображение')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    is_available = models.BooleanField(default=True, verbose_name='Доступность к заказу')

    category = models.ForeignKey(SportCategory, verbose_name='Категория', on_delete=models.PROTECT)
    product_types = models.ManyToManyField(ProductType, verbose_name='Типы товаров')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Бренд')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f"{self.name} - ({self.price} Рублей)"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart', verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"Корзина {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Корзина")
    product = models.ForeignKey(SportProduct, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name="Пользователь")
    product = models.ForeignKey(SportProduct, on_delete=models.CASCADE, verbose_name="Товар")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.product.name} в избранном у {self.user.username}"

# Новые таблицы для спорта и активного отдыха
class Warehouse(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование склада')
    address = models.TextField(verbose_name='Адрес')
    capacity = models.PositiveIntegerField(verbose_name='Вместимость (единиц)')

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f"{self.name} ({self.address})"

class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ('in', 'Поступление'),
        ('out', 'Списание'),
        ('transfer', 'Перемещение'),
    )
    product = models.ForeignKey(SportProduct, on_delete=models.CASCADE, verbose_name='Товар')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='Склад')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES, verbose_name='Тип движения')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')
    movement_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата движения')
    destination_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True, blank=True, related_name='destination_movements', verbose_name='Склад назначения')

    class Meta:
        verbose_name = 'Движение стока'
        verbose_name_plural = 'Движения стоков'

    def __str__(self):
        return f"{self.movement_type} {self.quantity} x {self.product.name} ({self.warehouse})"

class EquipmentFeature(models.Model):
    product = models.ForeignKey(SportProduct, on_delete=models.CASCADE, related_name='features', verbose_name='Товар')
    feature_name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название характеристики')
    feature_value = models.CharField(max_length=MAX_LENGTH, verbose_name='Значение характеристики')

    class Meta:
        verbose_name = 'Характеристика оборудования'
        verbose_name_plural = 'Характеристики оборудования'

    def __str__(self):
        return f"{self.feature_name}: {self.feature_value} для {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    email = models.EmailField(max_length=255, verbose_name='Электронная почта')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес доставки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    total_price = models.FloatField(verbose_name='Общая стоимость', default=0.0)
    status = models.CharField(max_length=50, default='pending', verbose_name='Статус')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.id} от {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey('SportProduct', on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')
    price = models.FloatField(verbose_name='Цена за единицу')

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f'{self.quantity} x {self.product.name} в заказе {self.order.id}'