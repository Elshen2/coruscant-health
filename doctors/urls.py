from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patients/', views.patient_list, name='doctor_patient_list'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('write-report/<int:patient_id>/', views.write_report, name='write_report'),
    path('orders/', views.my_orders, name='doctor_orders'),
    path('order/<int:patient_id>/', views.create_order, name='create_order'),
]