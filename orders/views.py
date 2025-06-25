from django.shortcuts import render

from orders.forms import OrderForm

def order(request):
    if request.method == 'POST':
        form = OrderForm(data=request.POST)
        if form.is_valid():
            ...
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

