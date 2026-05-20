from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from records.models import HealthRecord, DoctorReport
from departments.models import ServiceOrder
from .forms import DoctorReportForm, ServiceOrderForm

def doctor_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'doctor':
            messages.error(request, 'Bu səhifəyə giriş icazəniz yoxdur.')
            return redirect('dashboard')
        if not request.user.is_approved:
            return redirect('pending_approval')
        return view_func(request, *args, **kwargs)
    return wrapper

@doctor_required
def doctor_dashboard(request):
    # Təcili yardımdan gələn xəstələrin də görünməsi üçün is_approved=True süzgəci qaldırıldı
    patients = User.objects.filter(role='patient')
    orders   = ServiceOrder.objects.filter(ordered_by=request.user, status='pending')
    context  = {
        'patients_count': patients.count(),
        'orders_count':   orders.count(),
        'reports_count':  DoctorReport.objects.filter(doctor=request.user).count(),
        'recent_patients': patients[:5],
        'pending_orders':  orders[:5],
    }
    return render(request, 'doctors/dashboard.html', context)

@doctor_required
def patient_list(request):
    # Həkim bütün xəstələri siyahıda görə bilsin deyə filter yeniləndi
    patients = User.objects.filter(role='patient')
    return render(request, 'doctors/patient_list.html', {'patients': patients})

@doctor_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(User, id=patient_id, role='patient')
    records = HealthRecord.objects.filter(patient=patient)
    reports = DoctorReport.objects.filter(patient=patient)
    return render(request, 'doctors/patient_detail.html', {
        'patient': patient,
        'records': records,
        'reports': reports,
    })

@doctor_required
def write_report(request, patient_id):
    patient = get_object_or_404(User, id=patient_id, role='patient')
    form    = DoctorReportForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        report          = form.save(commit=False)
        report.doctor   = request.user
        report.patient  = patient
        report.save()
        messages.success(request, 'Hesabat uğurla yazıldı!')
        return redirect('patient_detail', patient_id=patient_id)
    return render(request, 'doctors/write_report.html', {
        'form': form, 'patient': patient
    })

@doctor_required
def my_orders(request):
    orders = ServiceOrder.objects.filter(ordered_by=request.user)
    return render(request, 'doctors/my_orders.html', {'orders': orders})

@doctor_required
def create_order(request, patient_id):
    patient = get_object_or_404(User, id=patient_id, role='patient')
    form    = ServiceOrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        order            = form.save(commit=False)
        order.ordered_by = request.user
        order.patient    = patient
        order.save()
        messages.success(request, 'Sifariş göndərildi!')
        return redirect('patient_detail', patient_id=patient_id)
    return render(request, 'doctors/create_order.html', {
        'form': form, 'patient': patient
    })