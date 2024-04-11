from django.db import models

# Create your models here.
class Company(models.Model):
    comp_name = models.CharField(max_length=100, null=True)
    comp_desc = models.CharField(max_length=1000, null=True)
    comp_logo = models.ImageField(upload_to='static/company/Images', default='static/company/Images/default.jpg', null=True)
    
    def __str__(self):
        return f"{self.comp_name}"
    pass