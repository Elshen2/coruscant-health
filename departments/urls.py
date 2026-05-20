from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.emergency_dashboard, name='emergency_dashboard'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/complete/<int:order_id>/', views.complete_order, name='complete_order'),
]