from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Reservation_App.views import (
    MainPageView,
    CreateSportPitchesView,
    CreateSportMatchesView,
    CityView,
    MatchDetails,
    DeleteListOfPlayer,
    DeleteMatch
)

class TestUrls(SimpleTestCase):
    def test_main_page_resolves(self):
        url = reverse("index")
        self.assertEquals(resolve(url).func.view_class, MainPageView)

    def test_create_ptich_url_resolves(self):
        url = reverse("pitch-create", args=["Kraków"])
        self.assertEquals(resolve(url).func.view_class, CreateSportPitchesView)

    def test_create_matchurl_resolves(self):
        url = reverse("match-create", args=["Kraków"])
        self.assertEquals(resolve(url).func.view_class, CreateSportMatchesView)

    def test_city_view_url_resolves(self):
        url = reverse("cityview", args=["Kraków"])
        self.assertEquals(resolve(url).func.view_class, CityView)

    def test_match_details_url_resolves(self):
        url = reverse("matchDetails", args=["Kraków", 1])
        self.assertEquals(resolve(url).func.view_class, MatchDetails)

    def test_delete_player_url_resolves(self):
        url = reverse("delete-from-list", args=[1])
        self.assertEquals(resolve(url).func.view_class, DeleteListOfPlayer)

    def test_delete_match_url_resolves(self):
        url = reverse("delete-match", args=[1])
        self.assertEquals(resolve(url).func.view_class, DeleteMatch)