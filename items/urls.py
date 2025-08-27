from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:id>/', views.item_detail, name='item_detail'),
    path('buy/<int:id>/', views.create_checkout_session, name='buy_item'),
    path('payment-intent/<int:id>/', views.create_payment_intent, name='payment_intent'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]