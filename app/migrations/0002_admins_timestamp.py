# Generated by Django 4.1.7 on 2023-11-18 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admins',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
