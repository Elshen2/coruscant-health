from django.urls import path
from . import views

urlpatterns = [
    path('my-records/', views.my_records, name='my_records'),
    path('upload/', views.upload_record, name='upload_record'),
]