# Generated by Django 4.2.13 on 2024-06-11 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_extenduser_first_name_extenduser_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extenduser',
            name='first_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='extenduser',
            name='last_name',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
