from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from company.models import Company

# Create your models here.

class User(AbstractUser):
    fname = models.CharField(max_length=100, null=True)
    lname = models.CharField(max_length=100, null=True)
    phone = models.CharField(validators=[MinLengthValidator(10)], max_length=10, null=True)
    user_photo = models.ImageField(upload_to='static/user_profiles/Images', null=True)
    followed_company = models.ManyToManyField(Company, related_name="following_user", blank=True)
    
    def serialize(self):
        return {
            'email': self.email,
            'fname': self.fname,
            'lname':self.lname,
            'phone':self.phone,
        }
class Major(models.Model):
    major_id = models.CharField(validators=[MinLengthValidator(3)], max_length=3, primary_key=True)
    major_desc = models.CharField(max_length=100, null=True)

    def serialize(self):
        return {
            'id': self.major_id,
            'desc': self.major_desc
        }
        
    def __str__(self):
        return f"{self.major_desc}"
class Professor(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='prof_user_id', null=True)
    major_id = models.ForeignKey(Major, on_delete=models.PROTECT, related_name='prof_major_id', null=True)
    
    def serialize(self):
        return {
            'major_id': self.major_id.major_id,
            'type': 'professor'
        }
        
    def __str__(self):
        return f"{self.user_id}"
class Employer(models.Model):
    prof_id = models.ForeignKey(Professor, on_delete=models.PROTECT, related_name='approve_prof_id', null=True)
    comp_id = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='comp_id', null=True)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='emp_user_id', null=True)
    emp_position = models.CharField(max_length=100, null=True)
    def serialize(self):
        return {
            'prof_id': self.prof_id,
            'comp_id': self.comp_id,
            'emp_position': self.emp_position,
            'type': 'employer'
        }
class Student(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='student_user_id', null=True)
    major_id = models.ForeignKey(Major, on_delete=models.PROTECT, related_name='student_major_id', null=True)
    student_resume = models.FileField(upload_to='static/user_profiles/Files', null=True)
    def serialize(self):
        return {
            'major_id': self.major_id.major_id,
            'type': 'student'
        }