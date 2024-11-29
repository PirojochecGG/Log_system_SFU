import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from inventory.models import Operation, Product
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Operation, Product, OperationProduct

@login_required
def products_view(request):
    products = Product.objects.all().order_by('code')
    context = {
        'show_header' : True,
        'products': products
    }
    return render(request, 'products.html', context)

@login_required
def prihod(request):
    operations = Operation.objects.filter(type='приход').order_by('date')
    context = {
        'show_header' : True,
        'operations': operations
    }
    return render(request, 'prihod.html', context)

@login_required
def rashod(request):
    operations = Operation.objects.filter(type='расход').order_by('date')
    context = {
        'show_header' : True,
        'operations': operations
    }
    return render(request, 'rashod.html', context)

@login_required
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

def welcome(request):
    return render(request, 'welcome.html', {'show_header': False})

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

@csrf_exempt # переделать сильно нужно будет
def add_product(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            qr_data = data.get("qr_data")
                        
            # Разделяем строки QR-кода
            lines = qr_data.strip().split('\n')
            
            # Обработка первой строки (данные операции)
            operation_info = lines[0].split(';')
            number, date, doc_date, operation_type, total_amount, amount_no_vat, partial_amount, counterparty, storage_location, no = operation_info

            # Создаем запись об операции
            operation = Operation.objects.create(
                number=number,
                date=date,
                doc_date=datetime.strptime(doc_date, '%Y-%m-%d'),
                type=operation_type,
                total_amount=total_amount,
                amount_no_vat=amount_no_vat,
                partial_amount=partial_amount,
                counterparty=counterparty,
                storage_location=storage_location
            )
            print(operation)
            
            # Обработка оставшихся строк (данные о товарах)
            for product_line in lines[1:]:
                product_info = product_line.split(';')

                code, name, quantity, unit, price, no = product_info
                
                quantity=float(quantity)
                price=float(price)
                total_price=quantity * price
                
                # Проверяем, существует ли товар с таким кодом
                existing_product = Product.objects.filter(code=code).first()
                
                if existing_product:
                    # Если товар существует, обновляем его актуальные данные
                    existing_product.quantity += quantity
                    existing_product.total_price += total_price
                    existing_product.save()

                    # Привязываем существующий товар к новой операции
                    Product.objects.create(
                        operation=operation,
                        code=code,
                        name=existing_product.name,
                        quantity=quantity,
                        unit=unit,
                        price=price,
                        total_price=total_price
                    )
                else:
                    # Если товар не существует, создаём новую запись
                    Product.objects.create(
                        operation=operation,
                        code=code,
                        name=name,
                        quantity=quantity,
                        unit=unit,
                        price=price,
                        total_price=total_price
                    )

            return JsonResponse({"message": "Операция и товары успешно добавлены!"})
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": str(e)}, status=400)
