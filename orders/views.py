from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.forms import ValidationError
from django.db import transaction
from django.utils import timezone
from django.db.models import Prefetch
from django.views.generic import FormView, TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from orders.forms import OrderForm
from orders.models import Order, OrderProduct
from users.models import User
from products.models import Product
from global_utils.mixins import CacheMixin
from orders.utils import get_order_items


class MakeOrderView(LoginRequiredMixin, FormView):
    template_name = 'order.html'
    form_class = OrderForm
    success_url = reverse_lazy('user:account')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        initial['phone_number'] = self.request.user.phone_number
        return initial
    
    def dispatch(self, request, *args, **kwargs):
        self.product_id = kwargs.get('product_id', None)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                phone_number = form.cleaned_data['phone_number']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                user_db = User.objects.filter(id=self.request.user.id)
                product_id = self.product_id

                if product_id:
                    user_order = Product.objects.get(id=product_id)
                    order = Order.objects.create(
                        user=user,
                        phone_number=phone_number,
                        requires_delivery=form.cleaned_data['requires_delivery'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        payment_on_get=form.cleaned_data['payment_on_get'],
                    )
                    OrderProduct.objects.create(order=order, product=user_order, name=user_order.name, price=user_order.price, quantity=1)
                else:
                    user_order = get_order_items(request=self.request)

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
                        
                        user_order.delete()
                
                if user.phone_number != phone_number:
                    user_db.update(phone_number=phone_number)
                
                if user.first_name != first_name:
                    user_db.update(first_name=first_name)
                
                if user.last_name != last_name:
                    user_db.update(last_name=last_name)
                
                if not product_id:
                    user_order.delete()

                return redirect('user:account')
            
        except ValidationError as e:
                return redirect('orders:order')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        return context


class UserOrdersView(CacheMixin, TemplateView):
    template_name = 'user_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваши заказы'

        orders = Order.objects.filter(user=self.request.user.id).prefetch_related(Prefetch("orderproduct_set", queryset=OrderProduct.objects.select_related('product')))
        context['orders'] = self.cache_data(orders, f'user_id{self.request.user.id}_orders', 2 * 60)
        return context


class CancelOrderView(View):
    def post(self, request):
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)

        order.status ='Отменён'
        order.cancellation_date = timezone.now()
        order.save()

        response = {
            "cancellation_date": order.cancellation_date.strftime("%d.%m.%Y %H:%M")
        }
        return JsonResponse(response)


class RepeatOrderView(View):
    def post(self, request):
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)

        order.status = 'В обработке'
        order.save()

        response = {
            "delivery_date": "(функция для подсчета времени доставки)",
        }

        return JsonResponse(response)