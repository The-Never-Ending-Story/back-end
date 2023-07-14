import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from worlds.models import World
from worlds.events.models import Event
from worlds.locations.models import Location
from worlds.characters.models import Character


@pytest.fixture
def mock_worlds():
    world1 = World.objects.create(
        name='Magic World',
        blurb='A magical world',
        description='A world of high fantasy and powerful magics',
        discovered=True,
        species={"origin": "human"},
        geoDynamics={"origin": "mountains"},
        magicTechnology={"origin": "ancient"},
        img='https://imgur.com/gallery/world123'
    )
    world2 = World.objects.create(
        name='Techno World',
        blurb='A technological world',
        description='A world of advanced technology',
        discovered=True,
        species={"origin": "human"},
        geoDynamics={"origin": "plains"},
        magicTechnology={"origin": "advanced"},
        img='https://imgur.com/gallery/world456'
    )
    return world1, world2


@pytest.fixture
def mock_events(mock_worlds, mock_locations):
    event1 = Event.objects.create(
        description='Fall of an empire',
        world_id=mock_worlds,
        location_id=mock_locations[0],
        time='200'
    )
    event2 = Event.objects.create(
        description='Start of a dynasty',
        world_id=mock_worlds,
        location_id=mock_locations[1],
        time='400'
    )
    event3 = Event.objects.create(
        description='Fall of an empire',
        world_id=mock_worlds,
        location_id=mock_locations[2],
        time='200'
    )
    event4 = Event.objects.create(
        description='Start of a dynasty',
        world_id=mock_worlds,
        location_id=mock_locations[3],
        time='400'
    )
    return event1, event2, event3, event4


@pytest.fixture
def mock_locations(mock_world):
    location1 = Location.objects.create(
        name='Magic City',
        attributes='magical',
        description='A magical city',
        img='https://imgur.com/gallery/location123',
        world_id=mock_worlds[0]
    )
    location2 = Location.objects.create(
        name='Techno City',
        attributes='technological',
        description='A technological city',
        img='https://imgur.com/gallery/location456',
        world_id=mock_worlds[0]
    )
    location3 = Location.objects.create(
        name='Magic City',
        attributes='magical',
        description='A magical city',
        img='https://imgur.com/gallery/location123',
        world_id=mock_worlds[1]
    )
    location4 = Location.objects.create(
        name='Techno City',
        attributes='technological',
        description='A technological city',
        img='https://imgur.com/gallery/location456',
        world_id=mock_worlds[1]
    )
    return location1, location2, location3, location4


@pytest.fixture
def mock_characters(mock_worlds, mock_locations):
    character1 = Character.objects.create(
        name='Joe Bob',
        race='human',
        alignment='lawful good',
        attributes='strong',
        description='A warrior',
        img='https://imgur.com/gallery/character123',
        world_id=mock_worlds[0],
        location_id=mock_locations[0]
    )
    character2 = Character.objects.create(
        name='Tim',
        race='human',
        alignment='lawful evil',
        attributes='smart',
        description='A mage',
        img='https://imgur.com/gallery/character456',
        world_id=mock_worlds[0],
        location_id=mock_locations[1]
    )
    character3 = Character.objects.create(
        name='Joe Bob',
        race='human',
        alignment='lawful good',
        attributes='strong',
        description='A warrior',
        img='https://imgur.com/gallery/character123',
        world_id=mock_worlds[1],
        location_id=mock_locations[2]
    )
    character4 = Character.objects.create(
        name='Tim',
        race='human',
        alignment='lawful evil',
        attributes='smart',
        description='A mage',
        img='https://imgur.com/gallery/character456',
        world_id=mock_worlds[1],
        location_id=mock_locations[3]
    )
    return character1, character2, character3, character4


@pytest.mark.django_db
def test_get_world_list_happy(mock_worlds):
    client = APIClient()
    url = reverse('get_world_list')
    response = client.get(url)

    assert response.status_code == 200
    world_list = response.json()
    assert len(world_list) == 2

    assert type(world_list) is list

    for world in world_list:
        assert 'id' in world
        assert 'name' in world
        assert 'blurb' in world
        assert 'description' in world
        assert 'species' in world
        assert 'geoDynamics' in world
        assert 'magicTechnology' in world
        assert 'img' in world
        assert 'history' in world
        assert 'events' in world
        assert 'locations' in world
        assert 'characters' in world

        assert type(world['id']) is int
        assert type(world['name']) is str
        assert type(world['blurb']) is str
        assert type(world['description']) is str
        assert type(world['species']) is dict
        assert type(world['geoDynamics']) is dict
        assert type(world['magicTechnology']) is dict
        assert type(world['img']) is str
        assert type(world['history']) is str
        assert type(world['events']) is list
        assert type(world['locations']) is list
        assert type(world['characters']) is list
