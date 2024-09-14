# Generated by Django 5.0.1 on 2024-04-11 16:31

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '__first__'),
        ('user_profiles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100)),
                ('job_type', models.CharField(choices=[('internship', 'Internship'), ('part time', 'Part Time'), ('full time', 'Full Time')], default='', max_length=10)),
                ('job_desc_text', models.CharField(blank=True, max_length=1000, null=True)),
                ('job_desc_file', models.FileField(blank=True, null=True, upload_to='static/job_post/files')),
                ('job_requirement_text', models.CharField(blank=True, max_length=1000, null=True)),
                ('job_requirement_file', models.FileField(blank=True, null=True, upload_to='static/job_post/files')),
                ('job_post_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('job_close_date', models.DateTimeField(blank=True, null=True)),
                ('job_location', models.CharField(blank=True, max_length=500, null=True)),
                ('job_status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='', max_length=10)),
                ('company', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='job_posts_by_company', to='company.company')),
                ('favourite_user', models.ManyToManyField(blank=True, related_name='favourite_posts', to=settings.AUTH_USER_MODEL)),
                ('job_major', models.ManyToManyField(related_name='job_posts_by_major', to='user_profiles.major')),
                ('poster_emp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_posted_by_emp', to='user_profiles.employer')),
                ('poster_prof', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_posted_by_prof', to='user_profiles.professor')),
            ],
        ),
    ]
