import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from worlds.models import World
from worlds.locations.models import Location
from worlds.events.models import Event


@pytest.fixture
def mock_world():
    return World.objects.create(
        name='Magic World',
        blurb='A magical world',
        description='A world of high fantasy and powerful magics',
        discovered=True,
        species={"origin": "human"},
        geodynamics={"origin": "mountains"},
        magictechnology={"origin": "ancient"},
        img='https://imgur.com/gallery/world123'
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
def mock_event(mock_world, mock_location):
    return Event.objects.create(
        description='Fall of an empire',
        world_id=mock_world,
        location_id=mock_location,
        time='200'
    )


@pytest.mark.django_db
def test_get_event_happy(mock_event, mock_world):
    client = APIClient()
    url_ids = {'world_id': mock_world.id, 'id': mock_event.id}

    url = reverse('get_world_event', kwargs=url_ids)
    response = client.get(url)

    assert response.status_code == 200
    json = response.json()

    assert type(json) is dict

    assert 'id' in json
    assert 'description' in json
    assert 'world_id' in json
    assert 'location_id' in json
    assert 'time' in json

    assert type(json['id']) is int
    assert type(json['description']) is str
    assert type(json['world_id']) is int
    assert type(json['location_id']) is int
    assert type(json['time']) is str
