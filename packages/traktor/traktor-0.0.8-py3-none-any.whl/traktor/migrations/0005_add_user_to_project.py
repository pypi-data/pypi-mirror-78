# Generated by Django 3.1 on 2020-08-28 20:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import traktor.models.user


class Migration(migrations.Migration):

    dependencies = [
        ("traktor", "0004_auto_20200823_1858"),
    ]

    operations = [
        migrations.RemoveField(model_name="entry", name="project",),
        migrations.AddField(
            model_name="project",
            name="user",
            field=models.ForeignKey(
                default=traktor.models.user.User.get_superuser_id,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
