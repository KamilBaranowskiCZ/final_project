from enum import unique
from nis import match
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User

from osm_field.fields import LatitudeField, LongitudeField, OSMField


class Cities(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class SportPitches(models.Model):
    name = models.CharField(max_length=70, unique=True)
    city = models.ForeignKey(Cities, on_delete=models.PROTECT, default=1)
    location = OSMField()
    location_lat = LatitudeField()
    location_lon = LongitudeField()

    def __str__(self):
        return self.name


class SportMatches(models.Model):
    pitch = models.ForeignKey(SportPitches, on_delete=models.PROTECT)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    gamedate = models.DateField()
    gametime = models.TimeField()
    max_num_of_players = models.IntegerField()

    def __str__(self):
        return f"{self.pitch} - {self.gamedate} - {self.gametime} - {self.max_num_of_players} graczy, stworzona przez {self.creator} "


class ListOfPlayers(models.Model):
    match = models.ForeignKey(SportMatches, on_delete=models.PROTECT)
    playerName = models.CharField(max_length=30)
