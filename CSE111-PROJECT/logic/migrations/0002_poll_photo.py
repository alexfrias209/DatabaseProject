# Generated by Django 4.1.7 on 2023-05-06 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='photo',
            field=models.ImageField(blank=True, upload_to='poll_photos/'),
        ),
    ]
