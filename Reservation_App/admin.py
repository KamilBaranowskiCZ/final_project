from django.contrib import admin
from .models import SportPitches, SportMatches, ListOfPlayers, MatchComments

# Register your models here.
admin.site.register(MatchComments)
admin.site.register(SportPitches)
admin.site.register(SportMatches)
admin.site.register(ListOfPlayers)