import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from worlds.models import World
from locations.models import Location


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


@pytest.mark.django_db
def test_get_location_happy(mock_location):
    client = APIClient()
    url = reverse('get_location', kwargs={'id': mock_location.id})
    response = client.get(url)

    assert response.status_code == 200
    location = response.json()

    assert type(location) is dict

    assert 'id' in location
    assert 'name' in location
    assert 'type' in location
    assert 'climate' in location
    assert 'lore' in location
    assert 'imagine' in location
    assert 'img' in location
    assert 'world' in location

    assert type(location['id']) is int
    assert type(location['name']) is str
    assert type(location['type']) is str
    assert type(location['climate']) is str
    assert type(location['lore']) is str
    assert type(location['imagine']) is str
    assert type(location['img']) is str
    assert type(location['world']) is int


@pytest.mark.django_db
def test_get_location_sad():
    client = APIClient()
    url = reverse('get_location', kwargs={'id': 5678})
    response = client.get(url)

    assert response.status_code == 404
