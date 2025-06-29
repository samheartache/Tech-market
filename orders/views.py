from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.forms import ValidationError
from django.db import transaction
from django.utils import timezone

from orders.forms import OrderForm
from orders.utils import get_order_items
from orders.models import Order, OrderProduct
from users.models import User

def order(request):
    if request.method == 'POST':
        form = OrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    user_order = get_order_items(request=request)
                    phone_number = form.cleaned_data['phone_number']
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    user_db = User.objects.filter(id=request.user.id)


                    if user_order.exists():
                        order = Order.objects.create(
                            user=user,
                            phone_number=phone_number,
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )

                        for prod in user_order:
                            product = prod.product
                            name = prod.product.name
                            price = prod.product.price
                            quantity = prod.quantity

                            OrderProduct.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )
                    
                    if user.phone_number != phone_number:
                        user_db.update(phone_number=phone_number)
                    
                    if user.first_name != first_name:
                        user_db.update(first_name=first_name)
                    
                    if user.last_name != last_name:
                        user_db.update(last_name=last_name)
                    
                    user_order.delete()

                    return redirect('user:account')
            except ValidationError as e:
                return redirect('orders:order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone_number': request.user.phone_number
        }

        form = OrderForm(initial=initial)
    
    context = {
        'title': 'Оформление заказа',
        'form': form,
    }
    return render(request, 'order.html', context=context)


def user_orders(request):
    orders = Order.objects.filter(user=request.user.id)

    context = {
        'title': 'Ваши заказы',
        'orders': orders
    }

    return render(request, 'user_orders.html', context=context)


def cancel(request):
    order_id = request.POST.get('order_id')
    order = Order.objects.get(id=order_id)

    order.status ='Отменён'
    order.cancellation_date = timezone.now()
    order.save()

    response = {
        "cancellation_date": order.cancellation_date.strftime("%d.%m.%Y %H:%M")
    }
    return JsonResponse(response)


def repeat(request):
    order_id = request.POST.get('order_id')
    order = Order.objects.get(id=order_id)

    order.status = 'В обработке'
    order.save()

    response = {
        "delivery_date": "(функция для подсчета времени доставки)",
    }

    return JsonResponse(response)

