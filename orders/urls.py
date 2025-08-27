from django.urls import path
from . import views

urlpatterns = [
    path('order/<int:id>/', views.order_detail, name='order_detail'),
    path('order/buy/<int:id>/', views.create_order_checkout_session, name='buy_order'),
]