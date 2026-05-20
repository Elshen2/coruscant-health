from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.utils import timezone
from accounts.models import User
from patients.models import PatientProfile
from .models import ServiceOrder

def emergency_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'emergency':
            messages.error(request, 'Bu panelə yalnız Təcili Yardım heyəti daxil ola bilər.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def department_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'department':
            messages.error(request, 'Bu panelə yalnız Şöbə/Laboratoriya heyəti daxil ola bilər.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

@emergency_required
def emergency_dashboard(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        birth_date = request.POST.get('birth_date')
        blood_group = request.POST.get('blood_group')
        symptoms = request.POST.get('symptoms')
        
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        username = f"pt_{get_random_string(5)}"
        
        try:
            new_user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                role='patient'
            )
            if birth_date:
                new_user.set_password(birth_date.replace('-', ''))
                new_user.save()
            
            PatientProfile.objects.create(
                user=new_user,
                date_of_birth=birth_date if birth_date else None,
                blood_type=blood_group,
                medical_history=symptoms if symptoms else ''
            )
            
            messages.success(request, f'{full_name} sistemə uğurla xəstə olaraq daxil edildi!')
        except Exception as e:
            messages.error(request, f'Qeydiyyat zamanı xəta baş verdi: {e}')
            
        return redirect('emergency_dashboard')

    recent_profiles = PatientProfile.objects.all().select_related('user').order_by('-id')[:10]
    today_count = PatientProfile.objects.count()
    pending_orders_count = ServiceOrder.objects.filter(status='pending').count()
    
    context = {
        'profiles': recent_profiles,
        'today_count': today_count,
        'pending_orders_count': pending_orders_count,
    }
    return render(request, 'departments/emergency_dashboard.html', context)

@department_required
def order_list(request):
    orders = ServiceOrder.objects.all().select_related('patient', 'ordered_by').order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'departments/order_list.html', context)

@department_required
def complete_order(request, order_id):
    order = get_object_or_404(ServiceOrder, id=order_id)
    
    if request.method == 'POST':
        result_text = request.POST.get('result')
        result_file = request.FILES.get('result_file')
        
        order.result = result_text if result_text else ''
        if result_file:
            order.result_file = result_file
            
        order.status = 'completed'
        order.completed_at = timezone.now()
        order.save()
        
        messages.success(request, f'#{order.id} nömrəli analiz/sifariş uğurla tamamlandı və nəticələr yükləndi.')
        return redirect('order_list')
        
    order.status = 'in_progress'
    order.save()
    
    context = {
        'order': order,
    }
    return render(request, 'departments/complete_order.html', context)