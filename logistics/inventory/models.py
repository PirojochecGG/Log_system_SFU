from django.db import models
from django.db.models import Sum, F

# Модель для операций
class Operation(models.Model):
    OPERATION_TYPES = [
        ('inflow', 'Приход'),
        ('outflow', 'Расход'),
    ]

    number = models.CharField(max_length=20, verbose_name="Номер", unique=True)
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    doc_date = models.DateTimeField(verbose_name="Дата документа", auto_now_add=True)
    type = models.CharField(max_length=10, choices=OPERATION_TYPES, verbose_name="Тип операции", default="outflow")
    counterparty = models.CharField(max_length=255, verbose_name="Контрагент", default="Неизвестный контрагент")
    storage_location = models.CharField(max_length=255, verbose_name="Место хранения", default="Не указано")

    @property
    def total_amount(self):
        total = self.operation_products.aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total']
        return total if total else 0

    def __str__(self):
        return f"{self.type} - {self.number} ({self.date})"

# Модель для товаров
class Product(models.Model):
    code = models.CharField(max_length=20, verbose_name="Код", default="000000")
    name = models.CharField(max_length=255, verbose_name="Название", default="Неизвестный товар")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество", default=0)
    unit = models.CharField(max_length=10, verbose_name="Единица измерения", default="шт")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена руб", default=0.0)
    
    @property
    def total_price(self):
        return self.quantity * self.price
    
    def __str__(self):
        return f"{self.name} ({self.code})"

# Модель для товаров для операции 
class OperationProduct(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name="operation_products", verbose_name="Операция")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="operation_product", verbose_name="Товар")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество")
    
    def __str__(self):
        return f"{self.operation} - {self.product.name}"
