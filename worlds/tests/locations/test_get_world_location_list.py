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
def mock_locations(mock_world):
    location1 = Location.objects.create(
        name='Magic City',
        type='city',
        climate='rainy',
        lore='An ancient city of wonder',
        imagine='Imagine a city of ancient magics',
        img='https://imgur.com/gallery/location123',
        world=mock_world
    )
    location2 = Location.objects.create(
        name='Techno City',
        type='city',
        climate='windy',
        lore='A futuristic city of advanced technology',
        imagine='Imagine a city of advanced technology',
        img='https://imgur.com/gallery/location456',
        world=mock_world
    )
    return location1, location2


@pytest.mark.django_db
def test_get_world_location_list_happy(mock_locations, mock_world):
    client = APIClient()
    url = reverse('get_world_location_list', kwargs={'id': mock_world.id})
    response = client.get(url)

    assert response.status_code == 200
    location_list = response.json()

    assert type(location_list) is list
    assert len(location_list) == 2

    for location in location_list:
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
