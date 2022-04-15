from ctypes import cdll
from nis import match
from unicodedata import name
from urllib import response
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth import login, authenticate, get_user
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, SportPitchesForm, SportMatchesForm, ListOfPlayerForm
from django import forms
from django.views.generic import CreateView, ListView
from .models import SportPitches, SportMatches, Cities, ListOfPlayers
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from datetime import datetime


class MainPageView(View):
    def get(self, request):
        return render(request, "main_page.html")


class CityView(View):
    def get(self, request, city):
        selected_city = Cities.objects.filter(name=city).first()
        allpitches = SportPitches.objects.filter(city_id=selected_city.id)
        all_matches = []
        for pitch in allpitches:
            one_pitch_matches = SportMatches.objects.filter(pitch_id=pitch.id).filter(gamedate__gte=datetime.today())
            all_matches.append(one_pitch_matches)
        return render(
            request,
            f"{city}.html",
            {"all_matches": all_matches, "selected_city": selected_city},
        )


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/")
    else:
        form = RegisterForm()
    return render(response, "register/register.html", {"form": form})


class CreateSportPitchesView(CreateView):
    template_name = "pitchcreate.html"
    form_class = SportPitchesForm
    model = SportPitches
    success_url = reverse_lazy("index")

    def get_initial(self):
        cityname = self.kwargs.get("city")
        if cityname == "Warszawa":
            return {"city": 2}
        elif cityname == "Kraków":
            return {"city": 1}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["location_lat"].widget = forms.HiddenInput()
        form.fields["location_lon"].widget = forms.HiddenInput()
        return form


class CreateSportMatchesView(CreateView):
    template_name = "games.html"
    form_class = SportMatchesForm
    model = SportMatches
    success_url = reverse_lazy("index")

    def get_initial(self):
        name = get_user(self.request)
        return {"creator": name}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["creator"].widget = forms.HiddenInput()
        cityname = self.kwargs.get("city")
        if cityname == "Warszawa":
            form.fields["pitch"].queryset = SportPitches.objects.filter(city=2)
        elif cityname == "Kraków":
            form.fields["pitch"].queryset = SportPitches.objects.filter(city=1)
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        obj = self.object
        obj.save()
        ListOfPlayers.objects.create(match_id=obj.id, playerName=get_user(self.request))
        return super().form_valid(form)


class MatchDetails(View):
    def get(self, request, city, sportmatches_id):
        match = get_object_or_404(SportMatches, pk=sportmatches_id)
        list_of_players = ListOfPlayers.objects.filter(match_id=sportmatches_id)
        player_counter = 0
        for player in list_of_players:
            player_counter += 1
        empty_places = match.max_num_of_players - player_counter
        name = get_user(self.request)
        print(empty_places)
        if empty_places > 0:
            form = ListOfPlayerForm(initial={'playerName': name, "match": match})
            form.fields["playerName"].widget = forms.HiddenInput()
            form.fields["match"].widget = forms.HiddenInput()
            return render(
                request,
                "matchDetail.html",
                {
                    "match": match,
                    "list_of_players": list_of_players,
                    "empty_places": empty_places,
                    "form": form
                },
            )
        else:
            return render(
                request,
                "matchDetailEmpty.html",
                {
                    "match": match,
                    "list_of_players": list_of_players,
                    "empty_places": empty_places,
                },
            )
    def post(self, request, city, sportmatches_id):
        form = ListOfPlayerForm(request.POST)
        if form.is_valid():
            new_player = ListOfPlayers.objects.create(match=form.cleaned_data['match'],
                                                 playerName=form.cleaned_data['playerName'],)
            return HttpResponseRedirect(self.request.path_info)
        