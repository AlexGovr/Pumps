# Generated by Django 3.1.5 on 2021-03-20 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_eqmark_mass'),
    ]

    operations = [
        migrations.AddField(
            model_name='eqmark',
            name='capacity',
            field=models.FloatField(default=-1),
        ),
    ]
