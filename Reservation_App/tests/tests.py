from django.test import Client
import pytest
from Reservation_App.models import Cities


def test_main_page():
    c = Client()
    response = c.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_cities_model(cityCracow, cityWarsaw):
    assert len(Cities.objects.all()) == 2
    assert Cities.objects.get(name="Kraków") == cityCracow
    assert Cities.objects.get(name="Warszawa") == cityWarsaw


# @pytest.mark.django_db
# def test_city_view(cityCracow):
#     c = Client()
#     city = Cities.objects.first()
#     print(city)
#     response = c.get('city/{city}/')
#     assert response.status_code == 200
