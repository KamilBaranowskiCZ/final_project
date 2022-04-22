from Reservation_App.models import Cities, SportPitches, SportMatches, User
import pytest


@pytest.fixture
def cityCracow():
    cityCracow = Cities.objects.get(name="Kraków")
    return cityCracow


@pytest.fixture
def cityWarsaw():
    cityWarsaw = Cities.objects.get(name="Warszawa")
    return cityWarsaw


@pytest.fixture
def createPitch():
    city = Cities.objects.get(name="Kraków")
    examplePitch = SportPitches.objects.create(
        name="Orlik",
        city_id=city.id,
        location="Szkoła Podstawowa nr 39 im. Bartosza Głowackiego",
        location_lat=50.062077900000006,
        location_lon=19.97754359627674
    )
    return examplePitch

@pytest.fixture
def createMatch():
    user = User.objects.create(username="ExampleUser")
    city = Cities.objects.get(name="Kraków")
    pitch = SportPitches.objects.create(
        name="Orlik",
        city_id=city.id,
        location="Szkoła Podstawowa nr 39 im. Bartosza Głowackiego",
        location_lat=50.062077900000006,
        location_lon=19.97754359627674
    )
    pitch.save
    exampleMatch = SportMatches.objects.create(
        pitch_id=pitch.id,
        creator_id=user.id,
        gamedate="2022-04-22",
        gametime="15:15:00",
        max_num_of_players=12
    )
    return exampleMatch