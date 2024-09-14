# Generated by Django 5.0.2 on 2024-04-19 06:06

import company.storage
import job_post.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("job_post", "0008_remove_jobpost_job_address_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jobpost",
            name="job_info_file",
            field=models.FileField(
                blank=True,
                null=True,
                storage=company.storage.OverwriteStorage(),
                upload_to=job_post.models.PathRename("job_post/job_info_file"),
            ),
        ),
    ]
