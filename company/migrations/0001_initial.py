# Generated by Django 4.2.9 on 2024-04-11 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp_name', models.CharField(max_length=100, null=True)),
                ('comp_desc', models.CharField(max_length=1000, null=True)),
                ('comp_logo', models.ImageField(default='static/company/Images/default.jpg', null=True, upload_to='static/company/Images')),
            ],
        ),
    ]
