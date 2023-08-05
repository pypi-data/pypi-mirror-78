# Generated by Django 3.1 on 2020-08-17 17:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(unique=True)),
                ("color", models.CharField(default="#000000", max_length=7)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="traktor.project",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField()),
                ("color", models.CharField(default="#000000", max_length=7)),
                ("default", models.BooleanField(default=False)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
            ],
            options={"unique_together": {("project", "slug")}},
        ),
        migrations.CreateModel(
            name="Entry",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="traktor.project",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="traktor.task",
                    ),
                ),
                ("description", models.CharField(default="", max_length=1023)),
                ("notes", models.TextField(default="")),
                ("start_time", models.DateTimeField(auto_now_add=True)),
                (
                    "end_time",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("duration", models.BigIntegerField(default=0)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
