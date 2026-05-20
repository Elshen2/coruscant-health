from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import LoginForm, RegisterForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            if not user.is_approved and not user.is_superuser:
                messages.warning(request, 'Hesabınız hələ təsdiqlənməyib. Admin təsdiqini gözləyin.')
                return redirect('pending_approval')
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username və ya şifrə yanlışdır.')

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_approved = False
        user.save()
        messages.success(request, 'Qeydiyyat uğurlu! Admin təsdiqini gözləyin.')
        return redirect('pending_approval')

    return render(request, 'accounts/register.html', {'form': form})


def pending_approval(request):
    return render(request, 'accounts/pending.html')


@login_required
def dashboard(request):
    user = request.user
    if user.is_superuser or user.role == 'admin':
        return redirect('/admin/')
    elif user.role == 'doctor':
        return redirect('doctor_dashboard')
    elif user.role == 'patient':
        return redirect('patient_dashboard')
    elif user.role == 'emergency':
        return redirect('emergency_dashboard')
    elif user.role == 'department':
        return redirect('order_list')
        
    return render(request, 'accounts/dashboard.html')


def simple_password_reset(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            
            messages.success(request, 'Şifrəniz uğurla yeniləndi! Yeni şifrə ilə daxil ola bilərsiniz.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Bu istifadəçi adı ilə qeydiyyat tapılmadı!')
            
    return render(request, 'accounts/password_reset_form.html')