# Generated by Django 5.0 on 2024-01-07 21:47

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='owner',
        ),
        migrations.AddField(
            model_name='food',
            name='day',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.macro_day'),
        ),
        migrations.AddField(
            model_name='food',
            name='name',
            field=models.CharField(default='', max_length=302, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='macro_day',
            name='date',
            field=models.DateField(default=datetime.date(2024, 1, 7), unique=True),
        ),
        migrations.AlterField(
            model_name='savedfood',
            name='food_name',
            field=models.TextField(default='', unique=True, verbose_name='Name'),
        ),
    ]
