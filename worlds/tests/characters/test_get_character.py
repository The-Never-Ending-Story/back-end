import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from fixtures.characters import mock_characters
from fixtures.worlds import mock_worlds


@pytest.mark.django_db
def test_get_character_valid(mock_characters):
    client = APIClient()
    url = reverse('get_character', kwargs={'id': mock_characters[0].id})
    response = client.get(url)

    assert response.status_code == 200
    character = response.json()

    assert type(character) is dict

    assert 'id' in character
    assert 'name' in character
    assert 'species' in character
    assert 'alignment' in character
    assert 'age' in character
    assert 'lore' in character
    assert 'imagine' in character
    assert 'img' in character
    assert 'imgs' in character
    assert 'location' in character
    assert 'world' in character

    assert type(character['id']) is int
    assert type(character['name']) is str
    assert type(character['species']) is str
    assert type(character['alignment']) is str
    assert type(character['age']) is int
    assert type(character['lore']) is str
    assert type(character['imagine']) is str
    assert type(character['img']) is str
    assert type(character['imgs']) is list
    assert type(character['location']) is str
    assert type(character['world']) is int


@pytest.mark.django_db
def test_get_character_invalid():
    client = APIClient()
    url = reverse('get_character', kwargs={'id': 5678})
    response = client.get(url)

    assert response.status_code == 404
