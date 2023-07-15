import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from worlds.models import World
from locations.models import Location
from characters.models import Character


@pytest.fixture
def mock_world():
    return World.objects.create(
        name='Magic World',
        blurb='A magical world',
        description='A world of high fantasy and powerful magics',
        discovered=False,
        geoDynamics={'origin': 'mountains'},
        magicTechnology={'origin': 'ancient'},
        img={'thumbnail': 'https://imgur.com/gallery/world123'}
    )


@pytest.fixture
def mock_location(mock_world):
    return Location.objects.create(
        name='Magic City',
        type='city',
        climate='rainy',
        lore='An ancient city of wonder',
        imagine='Imagine a city of ancient magics',
        img='https://imgur.com/gallery/location123',
        world=mock_world
    )


@pytest.fixture
def mock_character(mock_world, mock_location):
    return Character.objects.create(
        name='Joe Bob',
        species='human',
        alignment='lawful good',
        age=35,
        lore='A valiant warrior',
        imagine='Imagine a strong warrior',
        img='https://imgur.com/gallery/character123',
        location='The forest',
        world=mock_world,
    )


@pytest.mark.django_db
def test_get_character_valid(mock_character, mock_world):
    client = APIClient()
    url_ids = {'world_id': mock_world.id, 'id': mock_character.id}
    url = reverse('get_world_character', kwargs=url_ids)
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
    assert type(character['location']) is str
    assert type(character['world']) is int


@pytest.mark.django_db
def test_get_world_character_invalid_world(mock_character):
    client = APIClient()
    url_ids = {'world_id': 5678, 'id': mock_character.id}
    url = reverse('get_world_location', kwargs=url_ids)
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_get_world_character_invalid_character(mock_world):
    client = APIClient()
    url_ids = {'world_id': mock_world.id, 'id': 5678}
    url = reverse('get_world_location', kwargs=url_ids)
    response = client.get(url)

    assert response.status_code == 404
