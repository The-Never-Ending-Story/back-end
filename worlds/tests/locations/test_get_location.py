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
def mock_location(mock_world):
    return Location.objects.create(
        name='Magic City',
        attributes='magical',
        description='A magical city',
        img='https://imgur.com/gallery/location123',
        world_id=mock_world
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
