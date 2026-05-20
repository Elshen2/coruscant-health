from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import HealthRecord

@login_required
def my_records(request):
    if request.user.role != 'patient':
        messages.error(request, 'Bu səhifəyə yalnız xəstələr daxil ola bilər.')
        return redirect('dashboard')
        
    user_records = HealthRecord.objects.filter(patient=request.user).order_by('-recorded_at')
    
    context = {
        'records': user_records,
    }
    return render(request, 'patients/my_records.html', context)

@login_required
def upload_record(request):
    if request.user.role != 'patient':
        messages.error(request, 'Məlumat yükləmək icazəniz yoxdur.')
        return redirect('dashboard')
        
    if request.method == 'POST':
        heart_rate = request.POST.get('heart_rate')
        blood_pressure_sys = request.POST.get('blood_pressure_sys')
        blood_pressure_dia = request.POST.get('blood_pressure_dia')
        temperature = request.POST.get('temperature')
        oxygen_level = request.POST.get('oxygen_level')
        notes = request.POST.get('notes')
        
        try:
            HealthRecord.objects.create(
                patient=request.user,
                heart_rate=int(heart_rate) if heart_rate else None,
                blood_pressure_sys=int(blood_pressure_sys) if blood_pressure_sys else None,
                blood_pressure_dia=int(blood_pressure_dia) if blood_pressure_dia else None,
                temperature=float(temperature) if temperature else None,
                oxygen_level=float(oxygen_level) if oxygen_level else None,
                notes=notes if notes else ''
            )
            messages.success(request, 'Cihaz məlumatları uğurla bazaya yükləndi.')
            return redirect('my_records')
        except Exception as e:
            messages.error(request, f'Məlumat qeyd edilərkən xəta baş verdi: {e}')
            
    return render(request, 'patients/upload_record.html')