# Generated by Django 5.0.4 on 2024-05-17 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0011_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/static/assets1/img/profile_photos/'),
        ),
    ]
