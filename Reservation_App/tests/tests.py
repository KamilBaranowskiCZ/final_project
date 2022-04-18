from django.urls import reverse
from django.test import Client
import pytest
from Reservation_App.models import Cities, SportPitches, SportMatches


def test_main_page():
    c = Client()
    response = c.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_cities_model(cityCracow, cityWarsaw):
    assert len(Cities.objects.all()) == 2
    assert Cities.objects.get(name="Kraków") == cityCracow
    assert Cities.objects.get(name="Warszawa") == cityWarsaw

@pytest.mark.django_db
def test_pitch_model(createPitch):
    assert len(SportPitches.objects.all()) == 1
    assert SportPitches.objects.get(name="Orlik") == createPitch

@pytest.mark.django_db
def test_match_model(createMatch):
    assert len(SportMatches.objects.all()) == 1
    assert SportMatches.objects.get(gamedate="2022-04-22",) == createMatch


@pytest.mark.django_db
def test_city_view(cityCracow):
    c = Client()
    url = reverse('cityview', kwargs={'city': "Kraków"})
    response = c.get(url)
    assert response.status_code == 200
