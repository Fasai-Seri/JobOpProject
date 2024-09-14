from django import forms
from .models import Company
 
 
class CompanyForm(forms.ModelForm):
 
    class Meta:
        model = Company
        fields = ('comp_name','comp_name_th', 'comp_desc', 'comp_contact_info', 'comp_address', 'comp_lat', 'comp_long', 'comp_logo')