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
        self.delete_player_from_match_url = reverse("delete-from-list", args=[1])
        self.delete_match_url = reverse("delete-match", args=[1])

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
        cls.example_players_list = ListOfPlayers.objects.create(
            match=SportMatches.objects.get(id=1),
            playerName=User.objects.get(id=1),
        )
        cls.example_players_list_second_player = ListOfPlayers.objects.create(
            match=SportMatches.objects.get(id=1),
            playerName=User.objects.get(id=1),
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
        """get id and name of logged user"""
        self.client.login(username="testuser", password="userpass")
        logged_user_id = self.client.session["_auth_user_id"]
        logged_user_name = User.objects.get(id=logged_user_id)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        response = self.client.post(
            self.match_create_url,
            {
                "pitch": SportPitches.objects.get(id=1).id,
                "creator": logged_user_id,
                "gamedate": tomorrow,
                "gametime": "12:15:00",
                "max_num_of_players": 14,
            },
        )

        match_one = SportMatches.objects.get(id=2)
        self.assertEquals(match_one.creator, logged_user_name)
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
        """get name of logged user"""
        self.client.login(username="testuser", password="userpass")
        logged_user_id = self.client.session["_auth_user_id"]
        logged_user_name = User.objects.get(id=logged_user_id)
        """get id of current match"""
        match_id = self.match_details_url[-1]
        response = self.client.post(
            self.match_details_url,
            {
                "match": SportMatches.objects.get(id=match_id).id,
                "playerName": logged_user_name,
            },
        )

        list_of_players = ListOfPlayers.objects.get(id=match_id)

        self.assertEquals(list_of_players.playerName, logged_user_name.username)

    def test_match_detail_add_comment_POST(self):
        """get name of logged user"""
        self.client.login(username="testuser", password="userpass")
        logged_user_id = self.client.session["_auth_user_id"]
        logged_user_name = User.objects.get(id=logged_user_id)
        """get id of current match"""
        match_id = self.match_details_url[-1]
        response = self.client.post(
            self.match_details_url,
            {
                "match": SportMatches.objects.get(id=match_id).id,
                "name": logged_user_name,
                "body": "TestComment",
            },
        )

        comment = MatchComments.objects.get(id=1)
        self.assertEquals(comment.name, logged_user_name.username)
        self.assertEquals(comment.body, "TestComment")

    def test_delete_player_from_list_GET(self):
        """login user in order to fulfill view requierments"""
        self.client.login(username="testuser", password="userpass")
        list_of_players = ListOfPlayers.objects.all().count()
        self.assertEquals(list_of_players, 2)

        response = self.client.get(self.delete_player_from_match_url)

        list_of_players = ListOfPlayers.objects.all().count()
        self.assertEquals(response.status_code, 302)
        self.assertEquals(list_of_players, 1)

    def test_delete_match_GET(self):
        """login user in order to fulfill view requierments"""
        self.client.login(username="testuser", password="userpass")
        list_of_matches = SportMatches.objects.all().count()
        self.assertEquals(list_of_matches, 1)

        response = self.client.get(self.delete_match_url)

        list_of_matches = SportMatches.objects.all().count()

        self.assertEquals(response.status_code, 302)
        self.assertEquals(list_of_matches, 0)
