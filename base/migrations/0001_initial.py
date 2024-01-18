# Generated by Django 5.0 on 2024-01-18 17:23

import django.core.validators
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
            name='macro_day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default='2024-01-01')),
                ('weight', models.IntegerField(default=0)),
                ('calories', models.IntegerField(default=0)),
                ('pro', models.IntegerField(default=0)),
                ('fat', models.IntegerField(default=0)),
                ('carbs', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=302, verbose_name='Name')),
                ('cal', models.IntegerField(default=0, verbose_name='Calories')),
                ('protein', models.IntegerField(default=0)),
                ('carbs', models.IntegerField(default=0)),
                ('fat', models.IntegerField(default=0)),
                ('day', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.macro_day')),
            ],
        ),
        migrations.CreateModel(
            name='savedFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(default='', max_length=300)),
                ('cal_100g', models.IntegerField(default=0, verbose_name='Calories Per 100g')),
                ('protein_100g', models.IntegerField(default=0, verbose_name='Protein per 100g')),
                ('carb_100g', models.IntegerField(default=0, verbose_name='Carbohydrates per 100g')),
                ('fat_100g', models.IntegerField(default=0, verbose_name='Fat per 100g')),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='user_goals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal', models.CharField(choices=[('maintain', 'Maintain'), ('gain', 'Gain Weight'), ('lose', 'Lose Weight')], default='maintain', max_length=10)),
                ('experience', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner', max_length=25)),
                ('tdee', models.IntegerField(default=1000)),
                ('pRatio', models.IntegerField(default=50)),
                ('weekly_target', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('owner', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='macro_day',
            constraint=models.UniqueConstraint(fields=('owner', 'date'), name='Unique_tuple'),
        ),
        migrations.AddConstraint(
            model_name='savedfood',
            constraint=models.UniqueConstraint(fields=('owner', 'food_name'), name='unique_food_tuple'),
        ),
    ]
