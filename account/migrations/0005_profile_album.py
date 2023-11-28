# Generated by Django 4.2.7 on 2023-11-28 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("album", "0006_alter_album_options_and_more"),
        ("account", "0004_profile_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="album",
            field=models.ForeignKey(
                default=0, on_delete=django.db.models.deletion.CASCADE, to="album.album"
            ),
            preserve_default=False,
        ),
    ]
