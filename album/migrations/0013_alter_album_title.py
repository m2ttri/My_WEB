# Generated by Django 4.2.7 on 2023-12-17 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0012_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(max_length=18),
        ),
    ]
