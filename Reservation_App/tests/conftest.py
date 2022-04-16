from Reservation_App.models import Cities
import pytest


@pytest.fixture
def cityCracow():
    cityCracow = Cities.objects.create(name="Kraków")
    return cityCracow


@pytest.fixture
def cityWarsaw():
    cityWarsaw = Cities.objects.create(name="Warszawa")
    return cityWarsaw
