# Generated by Django 5.0 on 2024-01-15 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_user_goals_weekly_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='macro_day',
            name='carbs',
            field=models.IntegerField(default=0),
        ),
    ]