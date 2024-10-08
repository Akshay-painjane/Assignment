# Generated by Django 5.1.1 on 2024-09-27 06:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Field",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("visible_name", models.CharField(max_length=100)),
                ("data_type", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="TemplateMapping",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "destination_field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="destination_field",
                        to="attribute_app.field",
                    ),
                ),
                (
                    "source_field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="source_field",
                        to="attribute_app.field",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DataTemplate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "mappings",
                    models.ManyToManyField(
                        related_name="template_mappings",
                        to="attribute_app.templatemapping",
                    ),
                ),
            ],
        ),
    ]
