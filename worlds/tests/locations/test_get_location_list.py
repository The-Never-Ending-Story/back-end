import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from worlds.models import World
from worlds.locations.models import Location


@pytest.fixture
def mock_world():
    return World.objects.create(
        name='Magic World',
        blurb='A magical world',
        description='A world of high fantasy and powerful magics',
    )


@pytest.fixture
def mock_locations(mock_world):
    location1 = Location.objects.create(
        name='Magic City',
        attributes='magical',
        description='A magical city',
        img='https://imgur.com/gallery/location123',
        world_id=mock_world
    )
    location2 = Location.objects.create(
        name='Techno City',
        attributes='technological',
        description='A technological city',
        img='https://imgur.com/gallery/location456',
        world_id=mock_world
    )
    return location1, location2


@pytest.mark.django_db
def test_get_location_list_happy(mock_locations):
    client = APIClient()
    url = reverse('get_location_list')
    response = client.get(url)

    assert response.status_code == 200
    location_list = response.json()

    assert type(location_list) is list
    assert len(location_list) == 2

    for location in location_list:
        assert type(location) is dict

        assert 'id' in location
        assert 'attributes' in location
        assert 'description' in location
        assert 'img' in location
        assert 'world_id' in location
        assert 'type' in location

        assert type(location['id']) is int
        assert type(location['attributes']) is str
        assert type(location['description']) is str
        assert type(location['img']) is str
        assert type(location['world_id']) is int
        assert type(location['type']) is str
