# Generated by Django 4.2.7 on 2023-12-17 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_alter_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='users/no_image.jpg', upload_to='users/'),
        ),
    ]
