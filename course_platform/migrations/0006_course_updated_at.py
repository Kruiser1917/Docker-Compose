# Generated by Django 5.1.3 on 2024-12-03 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_platform', '0005_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
