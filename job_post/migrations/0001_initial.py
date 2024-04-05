# Generated by Django 5.0.1 on 2024-04-05 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=100)),
                ('post_desc', models.CharField(max_length=1000)),
                ('post_posted_date', models.DateField()),
                ('post_status', models.BooleanField()),
            ],
        ),
    ]