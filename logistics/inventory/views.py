import json
import urllib
import logging
import xlsxwriter
from io import BytesIO
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.db.models import IntegerField
from django.db.models.functions import Cast
from datetime import datetime
from decimal import Decimal
from .models import Operation, Product, OperationProduct

price_discrepancy_logger = logging.getLogger('price_discrepancies')

@login_required
@csrf_protect
def search_products(request):
    encoded_query = request.GET.get('query')
    query = urllib.parse.unquote(encoded_query) if encoded_query else ''
    
    print('\n', query, '\n')
    
    field = request.GET.get('field')
    
    if query and field:
        if field == "code":
            products = Product.objects.filter(code__icontains=query).order_by('code')
        elif field == "name":
            products = Product.objects.filter(name__icontains=query).order_by('code')
        elif field == "price":
            try:
                products = Product.objects.filter(price=float(query)).order_by('code')
            except ValueError:
                products = Product.objects.none()
        else:
            products = Product.objects.all().order_by('code')
    else:
        products = Product.objects.all().order_by('code')
    
    print(f"Найдено {len(products)} продуктов по запросу '{query}")
    
    return JsonResponse(list(products.values()), safe=False)
    
@login_required
@csrf_protect
def products_view(request):
    products = Product.objects.all().order_by('code')
    
    context = {
        'show_header' : True,
        'products': products
    }
    return render(request, 'products.html', context)

@login_required
@csrf_protect
def prihod(request):
    operations = Operation.objects.filter(type='приход') \
        .annotate(number_as_int=Cast('number', IntegerField())) \
        .order_by('number_as_int')
    context = {
        'show_header' : True,
        'operations': operations
    }
    return render(request, 'prihod.html', context)

@login_required
@csrf_protect
def rashod(request):
    operations = Operation.objects.filter(type='расход').order_by('date')
    context = {
        'show_header' : True,
        'operations': operations
    }
    return render(request, 'rashod.html', context)

@login_required
@csrf_protect
def get_products_by_operation(request, operation_id):
    operation = get_object_or_404(Operation, id=operation_id)
    
    operation_products = OperationProduct.objects.filter(operation=operation).select_related('product')
    
    products_data = [
        {
            'code': op.product.code,
            'name': op.product.name,
            'quantity': op.quantity,
            'unit': op.product.unit,
            'price': op.product.price,
            'total_price': round(op.quantity * op.product.price, 2)
        }
        for op in operation_products
    ]

    return JsonResponse({'products': products_data})

@csrf_protect
def welcome(request):
    return render(request, 'welcome.html', {'show_header': False})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            messages.success(request, "Вы успешно вошли в систему.")
            login(request, user)
            return redirect('/prihod')
        else:
           messages.error(request, 'Неверный email или пароль')
    return render(request, 'login.html', {'show_header': False})

@csrf_protect
def password_reset(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        
        subject = "Восстановление пароля"
        message = (
            f"Запрос на восстановление пароля от пользователя:\n\n"
            f"Имя: {first_name}\n"
            f"Фамилия: {last_name}\n"
            f"Email: {email}\n\n"
            f"Пожалуйста, свяжитесь с этим пользователем для восстановления доступа."
        )
        
        admin_email = settings.ADMIN_EMAIL
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
        )
        
        messages.success(request, "Ваш запрос отправлен. Мы свяжемся с вами в ближайшее время.")
        return redirect("login")

    return render(request, "password_reset.html")

@login_required
@csrf_protect
def add_product(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            qr_data = data.get("qr_data")
            
            lines = qr_data.strip().split('\n')
            
            operation_info = lines[0].split(';')
            (
                number, date, doc_date, operation_type, 
                counterparty, storage_location, _no
            ) = operation_info

            operation = Operation.objects.create(
                number=number,
                date=datetime.strptime(date, '%Y-%m-%d'),
                doc_date=datetime.strptime(doc_date, '%Y-%m-%d'),
                type=operation_type,
                counterparty=counterparty,
                storage_location=storage_location
            )

            for product_line in lines[1:]:
                product_info = product_line.split(';')

                code, name, quantity, unit, price, _no = product_info
                
                quantity = Decimal(quantity)
                price = price

                product, created = Product.objects.get_or_create(
                    code=code,
                    defaults={
                        'name': name,
                        'quantity': 0,
                        'unit': unit,
                        'price': price
                    }
                )

                if not created and product.price != price:
                    price_discrepancy_logger.warning(
                        f"Несоответствие цены для товара {code} ({name}): "
                        f"в базе {product.price}, в QR-коде {price}. "
                        f"Обновляем цену в БД."
                    )
                    product.price = price
                
                product.quantity += quantity
                product.save()
                
                OperationProduct.objects.create(
                    operation=operation,
                    product=product,
                    quantity=quantity
                )

            return JsonResponse({"message": "Операция и товары успешно добавлены!"})
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": str(e)}, status=400)
   
@login_required
@csrf_protect
def report_form(request):
    if request.method == 'POST':
        # Получаем номер операции из формы
        operation_number = request.POST.get('operation_number')
        
        # Проверяем наличие операции
        operation = get_object_or_404(Operation, number=operation_number)
        
        # Создаем Excel-отчет
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Отчет")
        
        # Стили
        bold = workbook.add_format({'bold': True})
        
        # Заголовки
        worksheet.write('A1', 'Номер операции', bold)
        worksheet.write('B1', 'Дата операции', bold)
        worksheet.write('C1', 'Тип операции', bold)
        worksheet.write('D1', 'Контрагент', bold)
        worksheet.write('E1', 'Товары', bold)
        
        # Данные операции
        worksheet.write('A2', operation.number)
        worksheet.write('B2', operation.date.strftime('%Y-%m-%d %H:%M:%S'))
        worksheet.write('C2', operation.get_type_display())
        worksheet.write('D2', operation.counterparty)
        
        # Данные товаров
        row = 4
        worksheet.write('E3', 'Товары', bold)
        worksheet.write('F3', 'Количество', bold)
        worksheet.write('G3', 'Цена за единицу', bold)
        worksheet.write('H3', 'Общая цена', bold)

        for product in operation.operation_products.all():
            worksheet.write(row, 4, product.product.name)
            worksheet.write(row, 5, float(product.quantity))
            worksheet.write(row, 6, float(product.product.price))
            worksheet.write(row, 7, float(product.quantity * product.product.price))
            row += 1

        workbook.close()
        output.seek(0)

        # Возвращаем файл
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="operation_{operation_number}.xlsx"'
        return response

    return render(request, 'genOtch.html', {'show_header': True})  