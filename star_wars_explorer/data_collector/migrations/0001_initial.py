# Generated by Django 5.0.6 on 2024-06-22 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StarWarsDataCollection",
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
                ("filename", models.CharField(max_length=255)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("edited", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
