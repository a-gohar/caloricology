# Generated by Django 5.0 on 2024-01-12 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_goals',
            name='experience',
            field=models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner', max_length=25),
        ),
        migrations.AddField(
            model_name='user_goals',
            name='goal',
            field=models.CharField(choices=[('maintain', 'Maintain'), ('gain', 'Gain Weight'), ('lose', 'Lose Weight')], default='maintain', max_length=10),
        ),
        migrations.AlterField(
            model_name='macro_day',
            name='date',
            field=models.DateField(default='2024-01-01', unique=True),
        ),
    ]