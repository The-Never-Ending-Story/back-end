import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from worlds.models import World
from events.models import Event
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


@pytest.fixture
def mock_characters(mock_world, mock_location):
    character1 = Character.objects.create(
        name='Joe Bob',
        race='human',
        alignment='lawful good',
        attributes='strong',
        description='A warrior',
        img='https://imgur.com/gallery/character123',
        world_id=mock_world,
        location_id=mock_location
    )
    character2 = Character.objects.create(
        name='Tim',
        race='human',
        alignment='lawful evil',
        attributes='smart',
        description='A mage',
        img='https://imgur.com/gallery/character456',
        world_id=mock_world,
        location_id=mock_location
    )
    return character1, character2


@pytest.mark.django_db
def test_get_world_happy(mock_world):
    client = APIClient()
    url = reverse('get_world', kwargs={'id': mock_world.id})
    response = client.get(url)

    assert response.status_code == 200
    world = response.json()

    assert type(world) is dict

    assert 'id' in world
    assert 'name' in world
    assert 'blurb' in world
    assert 'description' in world
    assert 'geoDynamics' in world
    assert 'magicTechnology' in world
    assert 'img' in world
    assert 'species' in world
    assert 'locations' in world
    assert 'characters' in world
    assert 'events' in world
    assert 'lore' in world

    assert type(world['id']) is int
    assert type(world['name']) is str
    assert type(world['blurb']) is str
    assert type(world['description']) is str
    assert type(world['geoDynamics']) is dict
    assert type(world['magicTechnology']) is dict
    assert type(world['img']) is dict
    assert type(world['species']) is list
    assert type(world['locations']) is list
    assert type(world['characters']) is list
    assert type(world['events']) is list
    assert type(world['lore']) is list


@pytest.mark.django_db
def test_get_world_sad():
    client = APIClient()
    url = reverse('get_world', kwargs={'id': 5678})
    response = client.get(url)

    assert response.status_code == 404
