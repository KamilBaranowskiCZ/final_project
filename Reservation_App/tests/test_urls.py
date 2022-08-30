import pytest

from django.urls import reverse

def test_main_view(client):
    url = reverse("index")
    response = client.get(url)
    assert response.status_code == 200


def test_register_view(client):
    url = reverse("register")
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_pitchCreate_view(client):
    url = reverse("pitch-create", kwargs={"city": "Kraków"})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_aboutmePage_view(client):
    url = reverse("match-create", kwargs={"city": "Kraków"})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_city_view(client):
    url = reverse("cityview", kwargs={"city": "Kraków"})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_match_detail_view(client,createMatch):
    url = reverse("matchDetails", kwargs={"city": "Kraków", "sportmatches_id": 1})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_match_view(client,createMatch):
    url = reverse("delete-match", kwargs={'match_id': createMatch.id})
    response = client.get(url)
    assert response.status_code == 302
