# Generated by Django 5.0.1 on 2024-04-16 16:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0004_remove_student_student_portfolio_portfolio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='student',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='portfolio_owner', to='user_profiles.student'),
        ),
    ]
