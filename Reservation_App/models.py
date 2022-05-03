from nis import match
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import datetime

from osm_field.fields import LatitudeField, LongitudeField, OSMField


class Cities(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class PitchType(models.Model):
    TYPESOFPITCH = (
        (1, "Hala"),
        (2, "Na świeżym powietrzu"),
        (3, "Pod balonem"),
        (4, "Trawiaste"),
        (5, "Sztuczna trawa"),
        (6, "Tartan"),
        (7, "Z szatnią"),
        (8, "Brak szatni"),

    )
    type = models.IntegerField(choices=TYPESOFPITCH)

    def __str__(self):
        return self.get_type_display()


class SportPitches(models.Model):
    name = models.CharField(max_length=70, unique=True)
    city = models.ForeignKey(Cities, on_delete=models.PROTECT, default=1)
    location = OSMField()
    location_lat = LatitudeField()
    location_lon = LongitudeField()
    pitches = models.ManyToManyField(PitchType, blank=True)

    def __str__(self):
        return self.name


class SportMatches(models.Model):
    pitch = models.ForeignKey(SportPitches, on_delete=models.PROTECT)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    gamedate = models.DateField(
        validators=[MinValueValidator(datetime.date.today)]
    )
    gametime = models.TimeField()
    max_num_of_players = models.IntegerField()

    def __str__(self):
        return f"""{self.pitch} - {self.gamedate} - {self.gametime} - {self.max_num_of_players} graczy, stworzona przez {self.creator}"""


class ListOfPlayers(models.Model):
    match = models.ForeignKey(SportMatches, on_delete=models.CASCADE)
    playerName = models.CharField(max_length=30)


class MatchComments(models.Model):
    match = models.ForeignKey(SportMatches, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

