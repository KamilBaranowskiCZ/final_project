from django.urls import reverse
from django.test import Client
import pytest
from Reservation_App.models import Cities, SportPitches, SportMatches


def test_main_page():
    c = Client()
    response = c.get("/")
    assert response.status_code == 200
    assert "Wybierz miasto" in str(response.content, "utf-8")


@pytest.mark.django_db
def test_cities_model():
    assert len(Cities.objects.all()) == 2
    assert Cities.objects.get(name="Kraków")
    assert Cities.objects.get(name="Warszawa")


@pytest.mark.django_db
def test_pitch_model(createPitch):
    assert len(SportPitches.objects.all()) == 1
    assert SportPitches.objects.get(name="Orlik") == createPitch


@pytest.mark.django_db
def test_match_model(createMatch):
    assert len(SportMatches.objects.all()) == 1
    assert (
        SportMatches.objects.get(
            gamedate="2022-04-22",
        )
        == createMatch
    )


@pytest.mark.django_db
def test_login_view():
    c = Client()
    response = c.post("/login/", {"username": "user", "password": "secret"})
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_pitch_view(createPitch):
    c = Client()
    url = reverse("pitch-create", kwargs={"city": "Kraków"})
    city = Cities.objects.get(name="Kraków")
    response = c.post(
        url,
        {
            "name": "Orlik",
            "city_id": city.id,
            "location": "Szkoła Podstawowa nr 39 im. Bartosza Głowackiego",
            "location_lat": 50.062077900000006,
            "location_lon": 19.97754359627674,
        },
    )
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_match_view(createMatch):
    c = Client()
    url = reverse("match-create", kwargs={"city": "Kraków"})
    response = c.post(
        url,
        {
            "pitch_id": createMatch,
            "creator_id": createMatch,
            "gamedate": "2022-04-22",
            "gametime": "15:15:00",
            "lmax_num_of_players": 12,
        },
    )
    assert response.status_code == 200