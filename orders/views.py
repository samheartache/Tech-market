from django.shortcuts import render

def order(request):
    context = {
        'title': 'Оформление заказа'
    }
    return render(request, 'order.html', context=context)
