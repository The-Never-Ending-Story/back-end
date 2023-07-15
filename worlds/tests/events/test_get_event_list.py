import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from worlds.models import World
from locations.models import Location
from events.models import Event


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
def mock_events(mock_world, mock_location):
    event1 = Event.objects.create(
        name='Fall of an empire',
        type='Downfall',
        age='Second Epoch',
        time='Year 250',
        lore='A significant event',
        imagine='Imagine a significant event',
        location='Capital of the empire',
        world=mock_world
    )
    event2 = Event.objects.create(
        name='Start of a dynasty',
        type='Rebirth',
        age='Third Epoch',
        time='Year 350',
        lore='Another significant event',
        imagine='Imagine another significant event',
        location='Capital of the empire',
        world=mock_world
    )
    return event1, event2


@pytest.mark.django_db
def test_get_event_list_happy(mock_events):
    client = APIClient()
    url = reverse('get_event_list')
    response = client.get(url)

    assert response.status_code == 200
    event_list = response.json()

    assert type(event_list) is list
    assert len(event_list) == 2

    for event in event_list:
        assert type(event) is dict

        assert 'id' in event
        assert 'name' in event
        assert 'type' in event
        assert 'age' in event
        assert 'time' in event
        assert 'lore' in event
        assert 'imagine' in event
        assert 'img' in event
        assert 'location' in event
        assert 'world' in event

        assert type(event['id']) is int
        assert type(event['name']) is str
        assert type(event['type']) is str
        assert type(event['age']) is str
        assert type(event['time']) is str
        assert type(event['lore']) is str
        assert type(event['imagine']) is str
        assert type(event['img']) is str
        assert type(event['location']) is str
        assert type(event['world']) is int
