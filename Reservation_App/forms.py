from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    SportPitches,
    SportMatches,
    ListOfPlayers,
    PitchType,
)
from .widgets import DatePickerInput, TimePickerInput


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
            "type",
        )
        model = SportPitches
        labels = {
            "name": "Nazwa",
            "city": "Miasto",
            "location": "Lokacja",
        }

    type = forms.ModelMultipleChoiceField(
        label="Szczegóły boiska",
        queryset=PitchType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class SportMatchesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SportMatchesForm, self).__init__(*args, **kwargs)
        self.fields["creator"].initial = User.username

    class Meta:
        fields = (
            "pitch",
            "creator",
            "gamedate",
            "gametime",
            "max_num_of_players",
        )
        model = SportMatches
        labels = {
            "pitch": "Boisko",
            "gamedate": "Data",
            "gametime": "Godzina rozpoczęcia",
            "max_num_of_players": "Liczba graczy",
        }
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
