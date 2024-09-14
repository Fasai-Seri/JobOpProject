# Generated by Django 5.0.1 on 2024-04-13 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_alter_company_comp_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='comp_address',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='comp_contact_info',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='comp_name_th',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
