from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address', 'contact_email', 'contact_phone', 'established_date', 'paye_reference_number', 'paye_office']
