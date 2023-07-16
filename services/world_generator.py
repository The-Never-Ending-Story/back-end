import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worlds.settings")
django.setup()

import json
from .api_services import gpt_response, dalle_image, imagine, get_progress
from .prompts import gpt_prompt
from .attributes import AESTHETICS, GEODYNAMICS
import random
from worlds.models import World, Event, Location, Character, Species
import time


def generate_random_world():
    attributes = random_attributes()
    print(attributes)
    world_response = gpt_response(gpt_prompt(attributes))
    print(world_response)

    try:
        world_json = json.loads(world_response)

        related_fields = ['species', 'characters', 'events', 'locations']
        world_info = {k: v for k, v in world_json.items() if k not in related_fields}
        world = World.objects.create(**world_info)

        for species in world_json.get('species', []):
            Species.objects.create(world=world, **species)

        for char in world_json.get('characters', []):
            Character.objects.create(world=world, **char)

        for event in world_json.get('events', []):
            Event.objects.create(world=world, **event)

        for location in world_json.get('locations', []):
            Location.objects.create(world=world, **location)

        world.save()
        add_midj_images(world)
        return world

    except json.JSONDecodeError as e:
        error = f"""
        Error decoding JSON: {e}
        Response text: {world_response}"
        """
        return error
    

def add_midj_images(world):
    thumbnail = landscape = {}

    if world.img.get("landscape"):
        thumbnail, landscape = world.img["thumbnail"], world.img["landscape"]
    else:
        while not thumbnail.get("success", False):
            thumbnail = imagine(
                {"model": "world", "id": world.id, "type": "thumbnail"},
                ' '.join(world.genres) + " landscape view of this world: " + world.imagine
            )
            if thumbnail.get("success", False):
                time.sleep(2)
                
        thumbnail = wait_for_image(thumbnail)["imageUrls"][0]
        
        while not landscape.get("success", False):
            landscape = imagine({"model": "world", "id": world.id, "type": "landscape"}, 
                thumbnail + " " + ' '.join(world.genres) + " " + world.imagine + " --iw .75 --ar 9:3")
            if landscape.get("success", False):
                time.sleep(2)
        
        landscape = wait_for_image(landscape)["imageUrls"][0]

    locations = world.locations.filter(img="none")
    locations_responses = []
    for location in locations:
        response = {}
        while not response.get("success", False):
            response = imagine({"model": "location", "id": location.id}, 
                thumbnail + " " + landscape + " " + 
                ' '.join(world.genres) + " " + location.imagine + " --iw .42 --ar 3:4")
            if response.get("success", False):
                time.sleep(2)
        locations_responses.append(response)
    
    for i in range(len(locations_responses)):
        locations_responses[i] = wait_for_image(locations_responses[i])

    print(locations)
            
    species_list = world.species.filter(img="none")
    species_responses = []
    for speciez in species_list:
        response = {}
        while not response.get("success", False):
            response = imagine({"model": "species", "id": speciez.id}, 
                thumbnail + " " + landscape + " " +
                ' '.join(world.genres) + " " + speciez.imagine + " --iw .55 --ar 3:4")
            time.sleep(2)
        species_responses.append(response)

    for i in range(len(species_responses)):
        species_responses[i] = wait_for_image(species_responses[i])

    chars = world.characters.filter(img="none")
    char_species = None
    for char in chars:
        try:
            char_species = world.species.get(name=char.species)
        except Species.DoesNotExist:
            try:
                char_species = world.species.get(name=char.species[:-1])
            except Species.DoesNotExist:
                char_species = None

        species_url = char_species.img if char_species else world.species.order_by('?').first().img
        location_url = world.locations.order_by('?').first().img

        response = {}
        while not response.get("success", False):
            response = imagine({"model": "character", "id": char.id}, 
                location_url + " " + species_url + " " +
                ' '.join(world.genres) + " " + char.imagine + " --iw .88 --ar 3:4")
            if response.get("success", False):
              time.sleep(2) 

    events = world.events.filter(img__isnull=True)
    for event in events:
        event_location = None
        try:
            event_location = world.locations.get(name=event.location)
        except Location.DoesNotExist:
            event_location = None

        response = {}
        location_url = event_location.img if event_location else world.locations.order_by('?').first().img
        species_url = char_species.img if char_species else world.species.order_by('?').first().img

        while not response.get("success", False):
            response = imagine({"model": "event", "id": event.id}, 
                location_url + " " + species_url + " " +
                ' '.join(world.genres) + " " + event.imagine + " --iw .42 --ar 3:4")
            time.sleep(2)


def wait_for_image(msg):
    if "messageId" in msg:
      if get_progress(msg["messageId"])["progress"] < 10:
        print("job started, brb...")
        time.sleep(42)
      update = get_progress(msg["messageId"])
      while not update["progress"] == 100:
            print(f'hol up, job cookin.. {update["progress"]}%')
            time.sleep(4)
            update = get_progress(msg["messageId"])

      print("ding! job finished.")
      return update["response"]
    
    else:
        return False

    
def random_attributes():
    earthly = random.choices(["earthly", "otherworldly"], weights=[0.42, 0.58], k=1)[0]
    return {
        "earthly": earthly_bool(earthly),
        "genres": aesthetics_sample(earthly),
        "geoDynamics": {
            "size": size_sample(earthly),
            "shape": shape_sample(earthly),
            "climate": climate_sample(earthly),
            "landscapes": landscapes_sample(earthly)
        },
        "magicTechnology": {
            "magicLvl": random.randint(0,10),
            "techLvl": random.randint(0,10),
        }
    }


def earthly_bool(earthly):
    return True if earthly == "earthly" else False


def aesthetics_sample(earthly):
    return random.sample(AESTHETICS[earthly], random.randint(1,3))


def size_sample(earthly):
    return random.sample(GEODYNAMICS["size"][earthly], 1)[0]


def shape_sample(earthly):
    return random.sample(GEODYNAMICS["shape"][earthly], 1)[0]


def climate_sample(earthly):
    return random.sample(GEODYNAMICS["climate"][earthly], 1)[0]
    

def landscapes_sample(earthly):
    if earthly == "earthly":
        return random.sample(GEODYNAMICS["landscapes"]["earthly"], random.randint(2,3))
    else:
        landscapes = []
        for _ in range(random.randint(2,3)):
            landscapes.append(random.sample(GEODYNAMICS["landscapes"][earthly], 1)[0] + " " + random.sample(GEODYNAMICS["landscapes"]["earthly"], 1)[0])
        return landscapes
    

def add_dalle_images(world):
        world["img"] = dalle_image(world["imagine"])
        for species in world["species"]:
            species["img"] = dalle_image(species["imagine"])
        for location in world["locations"]:
            location["img"] = dalle_image(location["imagine"])
        for char in world["characters"]:
            char["img"] = dalle_image(char["imagine"])
        for event in world["events"]:
            event["img"] = dalle_image(event["imagine"])
        
        return world

    
# world = generate_random_world()
# print(world)

world = World.objects.get(id=84)
add_midj_images(world)