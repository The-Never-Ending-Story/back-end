import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worlds.settings")
django.setup()

import json
from .api_services import gpt_response, dalle_image, imagine, upscale_img, get_progress
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
        print(world_json)

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
        add_midj_images(world.id)
        return world

    except json.JSONDecodeError as e:
        error = f"""
        Error decoding JSON: {e}
        Response text: {world_response}"
        """
        return error
    
def add_midj_images(world_id):
        world = World.objects.get(id=world_id)

        thumbnail = {}

        while not thumbnail.get("success", False):
            thumbnail = imagine({"model": "world", "id": world.id, "type": "thumbnail"}, 
                ' '.join(world.genres) + " landscape view of this world: " + world.imagine)
        print(thumbnail)
        thumbnail = wait_for_image(thumbnail)
        
        landscape = {}

        while not landscape.get("success", False):
            landscape = imagine({"model": "world", "id": world.id, "type": "landscape"}, 
                thumbnail["imageUrl"] + " " + ' '.join(world.genres) + " " + world.imagine + " --iw .75 --ar 9:3")
            
        landscape = wait_for_image(landscape)

        locations = []

        for location in world.locations.all():
            response = {}
            while not response.get("success", False):
                response = imagine({"model": "location", "id": location.id}, 
                    thumbnail["imageUrl"] + " " + landscape["imageUrl"] + " " + 
                    ' '.join(world.genres) + " " + location.imagine + " --iw .42 --ar 3:4")
                
            locations.append(response)
        
        wait_for_image(locations.last)

        species = []
        for species in world.species.all():
            response = {}
            while not response.get("success", False):
                response = imagine({"model": "species", "id": species.id}, 
                    thumbnail["imageUrl"] + " " + landscape["imageUrl"] + " " +
                    ' '.join(world.genres) + " " + species.imagine + " --iw .55 --ar 3:4")
            print(response)
            species.append(response)

        wait_for_image(species.last)

        chars = []
        for char in world.characters.all():
            try:
                species = world.species.get(name=char.species)
            except Species.DoesNotExist:
                try:
                    species = world.species.get(name=char.species[:-1])
                except Species.DoesNotExist:
                    species = None

            response = {}
            species_url = species.img if species else random.sample(world.species, 1)[0].img

            while not response.get("success", False):
                response = imagine({"model": "character", "id": char.id}, 
                    random.sample(locations, 1)[0]["imageUrl"] + " " + species_url +
                    ' '.join(world.genres) + " " + char.imagine + " --iw .88 --ar 3:4")
                
            chars.append(response)


def wait_for_image(msg):
    time.sleep(42)
    print(msg)
    if "messageId" in msg:
        update = get_progress(msg["messageId"])
        while not update["progress"] == 100:
            print("waiting for job to finish...")
            time.sleep(4)
            update = get_progress(msg["messageId"])

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

    
world = generate_random_world()
print(world)

# img = midjourney_image("a wormhole to another dimension")
# print(img)