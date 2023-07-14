import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from worlds.models import World
from worlds.locations.models import Location
from worlds.characters.models import Character


@pytest.fixture
def mock_world():
    return World.objects.create(
        name='Magic World',
        blurb='A magical world',
        description='A world of high fantasy and powerful magics',
    )


@pytest.fixture
def mock_location(mock_world):
    return Location.objects.create(
        name='Magic City',
        attributes='magical',
        description='A magical city',
        img='https://imgur.com/gallery/location123',
        world_id=mock_world
    )


@pytest.fixture
def mock_character(mock_world, mock_location):
    return Character.objects.create(
        name='Joe Bob',
        race='human',
        alignment='lawful good',
        attributes='strong',
        description='A warrior',
        img='https://imgur.com/gallery/character123',
        world_id=mock_world,
        location_id=mock_location
    )


@pytest.mark.django_db
def test_get_character_happy(mock_character, mock_world):
    client = APIClient()
    url_ids = {'world_id': mock_world.id, 'id': mock_character.id}
    url = reverse('get_world_character', kwargs=url_ids)
    response = client.get(url)

    assert response.status_code == 200
    character = response.json()

    assert type(character) is dict

    assert 'name' in character
    assert 'race' in character
    assert 'alignment' in character
    assert 'attributes' in character
    assert 'description' in character
    assert 'img' in character
    assert 'world_id' in character
    assert 'location_id' in character

    assert type(character['id']) is int
    assert type(character['name']) is str
    assert type(character['race']) is str
    assert type(character['alignment']) is str
    assert type(character['description']) is str
    assert type(character['img']) is str
    assert type(character['world_id']) is int
    assert type(character['location_id']) is int
