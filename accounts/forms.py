from django import forms
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'İstifadəçi adı',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Şifrə',
            'class': 'form-control'
        })
    )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Şifrə',
            'class': 'form-control'
        })
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Şifrəni təsdiqləyin',
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 
                  'email', 'phone', 'role']
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control'}),
            'phone':      forms.TextInput(attrs={'class': 'form-control'}),
            'role':       forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password_confirm')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Şifrələr uyğun deyil!')
        return cleaned_data