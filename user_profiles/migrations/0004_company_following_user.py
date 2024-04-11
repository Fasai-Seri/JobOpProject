# Generated by Django 4.2.9 on 2024-04-11 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0003_user_user_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='following_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followed_company', to=settings.AUTH_USER_MODEL),
        ),
    ]