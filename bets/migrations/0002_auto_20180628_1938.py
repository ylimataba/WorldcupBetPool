# Generated by Django 2.0.1 on 2018-06-28 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionPoints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveIntegerField()),
                ('gambler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bets.Gambler')),
            ],
        ),
        migrations.AlterModelOptions(
            name='betscore',
            options={'ordering': ['match', 'gambler']},
        ),
        migrations.AddField(
            model_name='betscore',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bets.Team'),
        ),
    ]