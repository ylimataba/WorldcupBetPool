# Generated by Django 2.0.1 on 2018-07-02 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0002_auto_20180628_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionpoints',
            name='competition',
            field=models.CharField(max_length=48, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bets.Team'),
        ),
    ]
