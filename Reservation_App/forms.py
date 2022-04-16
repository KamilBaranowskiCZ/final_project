from urllib import request
from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SportPitches, SportMatches, Cities, ListOfPlayers, PitchType
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
            'type'
        )
        model = SportPitches
    type = forms.ModelMultipleChoiceField(
        queryset=PitchType.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

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

class ListOfPlayerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ListOfPlayerForm, self).__init__(*args, **kwargs)
    class Meta:
        fields = ("match", "playerName")
        model = ListOfPlayers