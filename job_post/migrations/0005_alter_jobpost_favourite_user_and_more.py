# Generated by Django 4.2.9 on 2024-04-10 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profiles', '0003_user_user_photo'),
        ('job_post', '0004_alter_jobpost_poster_emp_alter_jobpost_poster_prof'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='favourite_user',
            field=models.ManyToManyField(blank=True, null=True, related_name='fovourite_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='job_close_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='job_desc',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='job_location',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='job_requirements',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='poster_emp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_posted_by_emp', to='user_profiles.employer'),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='poster_prof',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_posted_by_prof', to='user_profiles.professor'),
        ),
    ]
