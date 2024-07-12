# Generated by Django 4.2.13 on 2024-07-12 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppFeatures',
            fields=[
                ('feature_id', models.AutoField(primary_key=True, serialize=False)),
                ('feature_name', models.CharField(max_length=255)),
                ('feature_type', models.CharField(max_length=10)),
                ('feature_description', models.TextField()),
                ('feature_status', models.BooleanField()),
            ],
        ),
    ]
