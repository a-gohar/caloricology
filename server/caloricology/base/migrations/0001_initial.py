# Generated by Django 5.0 on 2024-01-05 17:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cal', models.IntegerField(default=0, verbose_name='Calories')),
                ('protein', models.IntegerField(default=0)),
                ('carbs', models.IntegerField(default=0)),
                ('fat_g', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='savedFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.TextField(default='', verbose_name='Name')),
                ('cal_100g', models.IntegerField(default=0, verbose_name='Calories Per 100g')),
                ('protein_100g', models.IntegerField(default=0, verbose_name='Protein per 100g')),
                ('carb_100g', models.IntegerField(default=0, verbose_name='Carbohydrates per 100g')),
                ('fat_100g', models.IntegerField(default=0, verbose_name='Fat per 100g')),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='weight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.PositiveSmallIntegerField(default='0')),
                ('entry_date', models.DateField(verbose_name='Date Entered')),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
