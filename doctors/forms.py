from django import forms
from records.models import DoctorReport
from departments.models import ServiceOrder

class DoctorReportForm(forms.ModelForm):
    class Meta:
        model = DoctorReport
        fields = ['title', 'content', 'prescription']
        widgets = {
            'title':        forms.TextInput(attrs={'class':'form-control'}),
            'content':      forms.Textarea(attrs={'class':'form-control','rows':5}),
            'prescription': forms.Textarea(attrs={'class':'form-control','rows':4,
                            'placeholder':'Dərman, doza, müddət...'}),
        }

class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = ['service_type', 'notes']
        widgets = {
            'service_type': forms.Select(attrs={'class':'form-select'}),
            'notes':        forms.Textarea(attrs={'class':'form-control','rows':3}),
        }