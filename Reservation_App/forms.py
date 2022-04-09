from urllib import request
from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SportPitches, SportMatches, Cities
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class SportPitchesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SportPitchesForm, self).__init__(*args, **kwargs)
        self.fields["city"].disabled = True

    class Meta:
        fields = (
            "name",
            "city",
            "location",
            "location_lat",
            "location_lon",
        )
        model = SportPitches


class SportMatchesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SportMatchesForm, self).__init__(*args, **kwargs)
        self.fields["creator"].initial = User.username

    class Meta:
        fields = ("pitch", "creator", "gamedate", "gametime", "max_num_of_players")
        model = SportMatches
        widgets = {
            "gamedate": DatePickerInput(),
            "gametime": TimePickerInput(),
        }
