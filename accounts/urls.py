from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('pending/', views.pending_approval, name='pending_approval'),
    path('password-reset/', views.simple_password_reset, name='password_reset'),
]