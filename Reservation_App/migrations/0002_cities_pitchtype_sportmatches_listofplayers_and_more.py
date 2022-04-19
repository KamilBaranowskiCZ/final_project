# Generated by Django 4.0.3 on 2022-04-19 21:22

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Reservation_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PitchType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Hala'), (2, 'Na świeżym powietrzu'), (3, 'Pod balonem'), (4, 'Trawiaste'), (5, 'Sztuczna trawa'), (6, 'Tartan'), (7, 'Z szatnią'), (8, 'Brak szatni')])),
            ],
        ),
        migrations.CreateModel(
            name='SportMatches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gamedate', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date.today)])),
                ('gametime', models.TimeField()),
                ('max_num_of_players', models.IntegerField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('pitch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Reservation_App.sportpitches')),
            ],
        ),
        migrations.CreateModel(
            name='ListOfPlayers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playerName', models.CharField(max_length=30)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reservation_App.sportmatches')),
            ],
        ),
        migrations.AddField(
            model_name='sportpitches',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='Reservation_App.cities'),
        ),
        migrations.AddField(
            model_name='sportpitches',
            name='pitches',
            field=models.ManyToManyField(blank=True, to='Reservation_App.pitchtype'),
        ),
    ]
