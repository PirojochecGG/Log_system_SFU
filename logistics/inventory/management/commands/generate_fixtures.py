from django.core.management.base import BaseCommand
from inventory.models import Product, Operation, OperationProduct
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate test data for products, operations, and operation products (100 records each)'

    def handle(self, *args, **kwargs):
        fake = Faker('ru_RU')
        
        # Очистка таблиц перед добавлением данных
        Product.objects.all().delete()
        Operation.objects.all().delete()
        OperationProduct.objects.all().delete()
        
        # Чтение списка названий товаров из файла
        file_path = 'products.txt'  # Укажи путь к своему файлу
        with open(file_path, 'r', encoding='utf-8') as file:
            product_names = [line.strip() for line in file if line.strip()]

        if not product_names:
            self.stdout.write(self.style.ERROR('Файл с товарами пуст или отсутствуют валидные строки.'))
            return
        
        # Создание товаров
        products = []
        for _ in range(100):
            name = random.choice(product_names)  # Случайный товар из списка
            product = Product.objects.create(
                code=fake.unique.ean(length=8),
                name=name,
                unit=random.choice(['шт', 'кг', 'л']),
                price=round(random.uniform(10, 1000), 2),
                quantity=random.randint(10, 100)
            )
            products.append(product)
        self.stdout.write(self.style.SUCCESS(f'Создано {len(products)} товаров.'))

        # Создание операций
        operations = []
        for _ in range(100):
            operation = Operation.objects.create(
                number=fake.unique.random_int(min=1000, max=9999),
                date=fake.date_this_year(),
                type=random.choice(['приход', 'расход']),
                counterparty=fake.company(),
                storage_location=fake.address()
            )
            operations.append(operation)
        self.stdout.write(self.style.SUCCESS(f'Создано {len(operations)} операций.'))

        # Связывание товаров с операциями
        for operation in operations:
            total_amount = 0
            for _ in range(random.randint(1, 5)):
                product = random.choice(products)
                quantity = random.randint(1, 10)
                total_price = product.price * quantity
                OperationProduct.objects.create(
                    operation=operation,
                    product=product,
                    quantity=quantity
                )
                total_amount += total_price

        self.stdout.write(self.style.SUCCESS('Данные успешно сгенерированы!'))
