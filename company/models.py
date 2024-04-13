from django.db import models

# Create your models here.
class Company(models.Model):
    comp_name = models.CharField(max_length=100, null=True)
    comp_desc = models.CharField(max_length=1000, null=True)
    comp_logo = models.ImageField(upload_to='company/Images', default='company/Images/default.jpg', null=True)
    comp_long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    comp_lat  = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    def __str__(self):
        return f"{self.comp_name}"
    
    def serialize(self) :
        if self.comp_logo:
            return {
                'comp_id': self.id,
                'comp_name': self.comp_name,
                'comp_desc': self.comp_desc,
                'comp_logo': self.comp_logo.url[1:],
            }
        else:
            return {
                'comp_name': self.comp_name,
                'comp_desc': self.comp_desc,
            }