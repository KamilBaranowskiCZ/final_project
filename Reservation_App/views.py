from ctypes import cdll
from urllib import response
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View 
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, SportPitchesForm, SportMatchesForm
from django import forms
from django.views.generic import CreateView, ListView
from .models import SportPitches, SportMatches, Cities
from django.urls import reverse_lazy, reverse
from random import shuffle


class MainPageView(View):
    def get(self, request):
        return render(request, 'main_page.html')


class CityView(View):
    def get(self, request, city):
        selected_city = Cities.objects.filter(name=city).first()
        allpitches = SportPitches.objects.filter(city_id=selected_city.id)
        all_matches = []
        for pitch in allpitches:
            one_pitch_matches = SportMatches.objects.filter(pitch_id=pitch.id)
            all_matches.append(one_pitch_matches)
        return render(request, f'{city}.html', {"all_matches": all_matches, "selected_city": selected_city})


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:    
        form = RegisterForm()
    return render(response, "register/register.html", {"form": form}) 




class CreateSportPitchesView(CreateView):
    template_name = "pitchcreate.html"
    form_class = SportPitchesForm
    model = SportPitches
    success_url = reverse_lazy("index")

    def get_initial(self):
            return { 'city': 2}
    

    def get_form(self, form_class=None):
        form = super().get_form( form_class)
        form.fields['location_lat'].widget = forms.HiddenInput()
        form.fields['location_lon'].widget = forms.HiddenInput()
        return form
    
    
class CreateSportMatchesView(CreateView):
    template_name = "games.html"
    form_class = SportMatchesForm
    model = SportMatches
    success_url = reverse_lazy("index")

    def get_form(self, form_class=None):
        form = super().get_form( form_class)
        form.fields['list_of_players'].widget = forms.HiddenInput()
        return form

class MatchDetails(View):
        def get(self, request, city, sportmatches_id):
            match = get_object_or_404(SportMatches, pk=sportmatches_id)
            return render(request, 'matchDetail.html', {"match": match})