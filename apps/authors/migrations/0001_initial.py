# Generated by Django 4.2.11 on 2024-05-02 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
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
                ("name", models.CharField(max_length=50)),
                ("lastname", models.CharField(blank=True, max_length=50)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
