# Generated by Django 4.2.13 on 2024-06-11 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_extenduser_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='extenduser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='extenduser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]