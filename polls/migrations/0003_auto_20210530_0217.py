# Generated by Django 2.2.23 on 2021-05-29 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20210530_0206'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='contractor',
            field=models.BooleanField(default=True),
        ),
    ]
