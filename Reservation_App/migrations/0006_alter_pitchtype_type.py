# Generated by Django 4.0.3 on 2022-04-16 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservation_App', '0005_alter_listofplayers_match_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pitchtype',
            name='type',
            field=models.IntegerField(choices=[(0, 'Hala'), (1, 'Na świeżym powietrzu'), (2, 'Pod balonem'), (3, 'Trawiaste'), (4, 'Sztuczna trawa'), (5, 'Tartan'), (6, 'Z szatnią'), (7, 'Brak szatni')]),
        ),
    ]
