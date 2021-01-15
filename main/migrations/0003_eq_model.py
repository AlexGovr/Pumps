# Generated by Django 3.0 on 2020-04-12 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_auto_20200412_1048'),
    ]

    operations = [
        migrations.CreateModel(
            name='Eq_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='Unnamed', max_length=60)),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.Manufacturer')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.Equipment_type')),
            ],
        ),
    ]
