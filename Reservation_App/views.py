from urllib import request
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth import get_user
from .forms import (
    RegisterForm,
    SportPitchesForm,
    SportMatchesForm,
    ListOfPlayerForm,
    CommentForm,
)
from django import forms
from django.views.generic import CreateView, DeleteView
from .models import SportPitches, SportMatches, Cities, ListOfPlayers, MatchComments
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from datetime import datetime


class MainPageView(View):
    def get(self, request):
        return render(request, "main_page.html")


class CityView(View):
    def get(self, request, city):
        '''displaying all matches in selected city'''
        selected_city = Cities.objects.filter(name=city).first()
        allpitches = SportPitches.objects.filter(city_id=selected_city.id)
        all_matches = []
        for pitch in allpitches:
            one_pitch_matches = SportMatches.objects.filter(
                pitch_id=pitch.id
            ).filter(gamedate__gte=datetime.today())
            all_matches.append(one_pitch_matches)
        '''adding coordiantes of all active matches'''
        all_coordinates = []
        for matches in all_matches:
            for one_match in matches:
                location_lat = str(one_match.pitch.location_lat)
                location_lon = str(one_match.pitch.location_lon)
                coordinates = location_lat + " , " + location_lon
                all_coordinates.append(coordinates)
        return render(
            request,
            f"{city}.html",
            {
                "all_matches": all_matches,
                "selected_city": selected_city,
                "all_coordinates": all_coordinates,
            },
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

    def get_success_url(self):
        return reverse_lazy("cityview", kwargs={"city": self.kwargs.get("city")})


    def get_initial(self):
        '''filling city field accordingly to url'''
        cityname = self.kwargs.get("city")
        if cityname == "Warszawa":
            return {"city": Cities.objects.get(name="Warszawa").id}
        elif cityname == "Kraków":
            return {"city": Cities.objects.get(name="Kraków").id}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["location_lat"].widget = forms.HiddenInput()
        form.fields["location_lon"].widget = forms.HiddenInput()
        return form


class CreateSportMatchesView(CreateView):
    template_name = "games.html"
    form_class = SportMatchesForm
    model = SportMatches

    def get_success_url(self):
        return reverse_lazy("cityview", kwargs={"city": self.kwargs.get("city")})

    def get_initial(self):
        '''filling creator field by logged user name'''
        name = get_user(self.request)
        return {"creator": name}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["creator"].widget = forms.HiddenInput()
        cityname = self.kwargs.get("city")
        if cityname == "Warszawa":
            form.fields["pitch"].queryset = SportPitches.objects.filter(city=Cities.objects.get(name="Warszawa").id)
        elif cityname == "Kraków":
            form.fields["pitch"].queryset = SportPitches.objects.filter(city=Cities.objects.get(name="Kraków").id)
        return form


    # create list of player to created game and add creator as first user at this list
    def form_valid(self, form):
        super().form_valid(form)
        obj = self.object
        obj.save()
        ListOfPlayers.objects.create(
            match_id=obj.id, playerName=get_user(self.request)
        )
        return super().form_valid(form)


class MatchDetails(View):
    def get(self, request, city, sportmatches_id):
        match = get_object_or_404(SportMatches, pk=sportmatches_id)
        list_of_players = ListOfPlayers.objects.filter(
            match_id=sportmatches_id
        )
        '''counter of empty places at list of player list'''
        player_counter = 0
        for player in list_of_players:
            player_counter += 1
        empty_places = match.max_num_of_players - player_counter
        name = get_user(self.request)
        location_lat = str(match.pitch.location_lat)
        location_lon = str(match.pitch.location_lon)
        comment_form = CommentForm(
            initial={"name": name, "match": match})
        comment_form.fields["match"].widget = forms.HiddenInput()
        
        comment_form.fields["name"].widget = forms.HiddenInput()
        if empty_places > 0:
            '''render html when game has empty spots'''
            form = ListOfPlayerForm(
                initial={"playerName": name, "match": match}
            )
            form.fields["playerName"].widget = forms.HiddenInput()
            form.fields["match"].widget = forms.HiddenInput()
            return render(
                request,
                "matchDetail.html",
                {
                    "match": match,
                    "list_of_players": list_of_players,
                    "empty_places": empty_places,
                    "form": form,
                    "location_lat": location_lat,
                    "location_lon": location_lon,
                    "comment_form": comment_form
                },
            )
        
        else:
            '''render html when game hasn't empty spots'''
            return render(
                request,
                "matchDetailEmpty.html",
                {
                    "match": match,
                    "list_of_players": list_of_players,
                    "empty_places": empty_places,
                    "location_lat": location_lat,
                    "location_lon": location_lon,
                },
            )
    def post(self, request, city, sportmatches_id):
        '''adding logged user to game list of players'''
        form = ListOfPlayerForm(request.POST)
        comment_form = CommentForm(request.POST)
        if form.is_valid():
            ListOfPlayers.objects.create(
                match=form.cleaned_data["match"],
                playerName=form.cleaned_data["playerName"],
            )
            return HttpResponseRedirect(self.request.path_info)
        if comment_form.is_valid():
            MatchComments.objects.create(
                match=comment_form.cleaned_data["match"],
                name=comment_form.cleaned_data["name"],
                body=comment_form.cleaned_data["body"],
            )
            return HttpResponseRedirect(self.request.path_info)

class DeleteListOfPlayer(View):
    def get(self, request, list_of_players_id):
        '''delete player from player list in game, player only remove himself'''
        playerslist = ListOfPlayers.objects.get(id=list_of_players_id)
        if str(playerslist.playerName) == str(get_user(self.request)):
            playerslist.delete()
        return redirect(request.META.get('HTTP_REFERER'))


class DeleteMatch(View):
    def get(self, request, match_id):
        '''delete game only by creator'''
        match_to_delete = SportMatches.objects.get(id=match_id)
        if str(match_to_delete.creator) == str(get_user(self.request)):
            match_to_delete.delete()
        return redirect("index")