# Generated by Django 4.2 on 2023-12-05 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logic', '0008_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='poll_photos/picTest.jpg', null=True, upload_to='profiles/'),
        ),
    ]
