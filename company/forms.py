from django import forms
from .models import Company
 
 
class CompanyForm(forms.ModelForm):
 
    class Meta:
        model = Company
        fields = ('comp_name', 'comp_desc')