from urllib import response
from django.test import TestCase, Client
from django.urls import reverse
from Reservation_App.models import (
    SportPitches,
    SportMatches,
    Cities,
    ListOfPlayers,
    MatchComments,
    PitchType,
)
from django.contrib.auth.models import User
import datetime


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.main_page_url = reverse("index")
        self.city_view_url = reverse("cityview", args=["Kraków"])
        self.pitch_create_url = reverse("pitch-create", args=["Kraków"])
        self.match_create_url = reverse("match-create", args=["Kraków"])
        self.match_details_url = reverse("matchDetails", args=["Kraków", 1])

    #     self.room_details_url = reverse("room-details", args=[1])
    #     self.room_search_url = reverse("room-search")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", email="user@user.com", password="userpass"
        )
        cls.example_pitch = SportPitches.objects.create(
            name="ExamplePitch",
            city=Cities.objects.get(name="Kraków"),
            location="ExamplePlace",
            location_lat=40.00,
            location_lon=50.40,
        )
        cls.example_match = SportMatches.objects.create(
            pitch=SportPitches.objects.get(id=1),
            creator=User.objects.get(id=1),
            gamedate=datetime.date.today() + datetime.timedelta(days=1),
            gametime="12:15:00",
            max_num_of_players=12,
        )

    def test_main_page_GET(self):
        response = self.client.get(self.main_page_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "main_page.html")

    def test_city_view_GET(self):
        response = self.client.get(self.city_view_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "Kraków.html")

    def test_pitch_create_GET(self):
        response = self.client.get(self.pitch_create_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "pitchcreate.html")

    def test_pitch_create_POST(self):
        response = self.client.post(
            self.pitch_create_url,
            {
                "name": "PitchExample",
                "city": Cities.objects.get(name="Kraków").id,
                "location": "LocationExample",
                "location_lat": 40.00,
                "location_lon": 50.40,
                "pitch": [1, 2, 3],
            },
        )
        pitch_one = SportPitches.objects.get(id=2)

        self.assertEquals(pitch_one.name, "PitchExample")
        self.assertEquals(str(pitch_one.pitches.first()), "Hala")

    def test_match_create_GET(self):
        response = self.client.get(self.match_create_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "games.html")

    def test_match_create_POST(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        response = self.client.post(
            self.match_create_url,
            {
                "pitch": SportPitches.objects.get(id=1).id,
                "creator": User.objects.get(id=1).id,
                "gamedate": tomorrow,
                "gametime": "12:15:00",
                "max_num_of_players": 14,
            },
        )

        match_one = SportMatches.objects.get(id=2)

        self.assertEquals(str(match_one.gametime), "12:15:00")
        self.assertEquals(str(match_one.gamedate), str(tomorrow))
        self.assertEquals(match_one.max_num_of_players, 14)
        """check is list of player was created"""
        self.assertEquals(
            ListOfPlayers.objects.get(match_id=match_one.id).match_id, match_one.id
        )

    def test_match_details_GET(self):
        response = self.client.get(self.match_details_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "matchDetail.html")

    def test_match_detail_add_player_POST(self):
        """get id of current match"""
        match_id = self.match_details_url[-1]
        response = self.client.post(
            self.match_details_url,
            {
                "match": SportMatches.objects.get(id=match_id).id,
                "playerName": "RandomUser",
            },
        )

        list_of_players = ListOfPlayers.objects.get(id=2)

        self.assertEquals(list_of_players.playerName, "RandomUser")
