from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('upload-record/', views.upload_record, name='upload_record'),
    path('records/', views.my_records, name='my_records'),
    path('reports/', views.my_reports, name='my_reports'),
    path('documents/', views.my_documents, name='my_documents'),
    path('upload-document/', views.upload_document, name='upload_document'),
]