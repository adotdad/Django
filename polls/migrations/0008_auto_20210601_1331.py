# Generated by Django 2.2.23 on 2021-06-01 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_newuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]
