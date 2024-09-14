from django import forms
from .models import User, Student
 
 
class UserForm(forms.ModelForm):
 
    class Meta:
        model = User
        fields = ('fname', 'lname', 'phone', 'user_photo')