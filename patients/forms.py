from django import forms
from records.models import HealthRecord, MedicalDocument

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['heart_rate', 'blood_pressure_sys', 'blood_pressure_dia',
                  'temperature', 'oxygen_level', 'notes']
        widgets = {
            'heart_rate':         forms.NumberInput(attrs={'class':'form-control','placeholder':'məs: 72'}),
            'blood_pressure_sys': forms.NumberInput(attrs={'class':'form-control','placeholder':'məs: 120'}),
            'blood_pressure_dia': forms.NumberInput(attrs={'class':'form-control','placeholder':'məs: 80'}),
            'temperature':        forms.NumberInput(attrs={'class':'form-control','placeholder':'məs: 36.6','step':'0.1'}),
            'oxygen_level':       forms.NumberInput(attrs={'class':'form-control','placeholder':'məs: 98','step':'0.1'}),
            'notes':              forms.Textarea(attrs={'class':'form-control','rows':3}),
        }

class MedicalDocumentForm(forms.ModelForm):
    class Meta:
        model = MedicalDocument
        fields = ['title', 'document_type', 'file']
        widgets = {
            'title':         forms.TextInput(attrs={'class':'form-control'}),
            'document_type': forms.Select(attrs={'class':'form-select'}),
            'file':          forms.FileInput(attrs={'class':'form-control'}),
        }