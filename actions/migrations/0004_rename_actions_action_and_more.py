# Generated by Django 4.2.7 on 2023-11-30 18:41

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenttypes", "0002_remove_content_type_name"),
        ("actions", "0003_rename_action_actions_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Actions",
            new_name="Action",
        ),
        migrations.RenameIndex(
            model_name="action",
            new_name="actions_act_created_64f10d_idx",
            old_name="actions_act_created_639f69_idx",
        ),
        migrations.RenameIndex(
            model_name="action",
            new_name="actions_act_target__f20513_idx",
            old_name="actions_act_target__5ecc2e_idx",
        ),
    ]
