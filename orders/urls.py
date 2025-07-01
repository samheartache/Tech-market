from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('order/<int:product_id>/', views.MakeOrderView.as_view(), name='single_order'),
    path('order/', views.MakeOrderView.as_view(), name='order'),
    path('userorders/', views.UserOrdersView.as_view(), name='userorders'),
    path('cancel/', views.CancelOrderView.as_view(), name='cancel'),
    path('repeat/', views.RepeatOrderView.as_view(), name='repeat'),
]