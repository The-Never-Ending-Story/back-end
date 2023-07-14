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
def mock_events(mock_world, mock_location):
    event1 = Event.objects.create(
        description='Fall of an empire',
        world_id=mock_world,
        location_id=mock_location,
        time='200'
    )
    event2 = Event.objects.create(
        description='Start of a dynasty',
        world_id=mock_world,
        location_id=mock_location,
        time='400'
    )
    return event1, event2


@pytest.mark.django_db
def test_get_event_happy(mock_events):
    client = APIClient()
    url = reverse('get_event_list')
    response = client.get(url)

    assert response.status_code == 200
    json = response.json()

    assert type(json) is list
    assert len(json) == 2
    event = json[0]

    assert type(event) is dict

    assert 'id' in event
    assert 'description' in event
    assert 'world_id' in event
    assert 'location_id' in event
    assert 'time' in event

    assert type(event['id']) is int
    assert type(event['description']) is str
    assert type(event['world_id']) is int
    assert type(event['location_id']) is int
    assert type(event['time']) is str
