import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worlds.settings")
django.setup()

import json
from .api_services import gpt_response, dalle_image, imagine, get_progress, upscale_img
from .prompts import gpt_prompt
from .attributes import random_attributes
from django.db.models import Q
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
    print(f'working on landscapes for world {world.id}...')
    
    world_img = world.img
    world_imgs = world.imgs if isinstance(world.imgs, dict) else {}

    thumbnail = world_img.get("thumbnail")
    landscape = world_img.get("landscape")

    if thumbnail is not None and isinstance(thumbnail, str) and thumbnail.startswith("https"):
        if "thumbnails" not in world_imgs or not len(world_imgs["thumbnails"]) == 4:
            base_url = thumbnail[-1:]
            world_imgs["thumbnails"] = [base_url + "0", base_url + "1", base_url + "2", base_url + "3"]
    
    elif thumbnail is not None and isinstance(thumbnail, str):
        try: 
            thumbnail = upscale_img(thumbnail)
            if isinstance(thumbnail, str) and thumbnail.startswith('https'):
                world.img["thumbnail"] = thumbnail
                base_url = thumbnail[-1:]
                world_imgs["thumbnails"] = [base_url + "0", base_url + "1", base_url + "2", base_url + "3"]
        except: 
            thumbnail = None

    elif thumbnail is None or not isinstance(thumbnail, str) or thumbnail == "none":
        thumbnail = {}
        while not thumbnail.get("success", False):
            thumbnail = imagine(
                {"model": "world", "id": world.id, "type": "thumbnail"},
                ' '.join(world.genres) + " landscape view of this world: " + world.imagine
            )
            if thumbnail.get("success", False):
                time.sleep(2)

        thumbnail = wait_for_image(thumbnail)
        if thumbnail != "none":
            world_imgs["thumbnails"] = thumbnail["imageUrls"]
            world_img["thumbnail"] = thumbnail = thumbnail["imageUrls"][0]
        else:
            thumbnail = world_img["thumbnail"] = "none"
            world_imgs["thumbnails"] = []
    else: 
        thumbnail = world_img["thumbnail"] = "none"


    if landscape is not None and isinstance(landscape, str) and landscape.startswith("https"):
        if "landscapes" not in world.imgs or not len(world.imgs["landscapes"]) == 4:
            base_url = landscape[-1:]
            world_imgs["landscapes"] = [base_url + "0", base_url + "1", base_url + "2", base_url + "3"]
    
    elif landscape is not None and isinstance(landscape, str):
        try: 
            landscape = upscale_img(landscape)
            if isinstance(landscape, str) and landscape.startswith('https'):
                world_img["landscape"] = landscape
                base_url = landscape[-1:]
                world_imgs["landscapes"] = [base_url + "0", base_url + "1", base_url + "2", base_url + "3"]
        except: 
            landscape = None

    elif landscape is None or landscape == "none" or not isinstance(landscape, str):
        landscape = {}
        while not landscape.get("success", False):
            landscape = imagine(
                {"model": "world", "id": world.id, "type": "landscape"},
                thumbnail + " " + ' '.join(world.genres) + " " + world.imagine + " --iw .75 --ar 9:3"
            )
            if landscape.get("success", False):
                time.sleep(2)

        landscape = wait_for_image(landscape)
        if landscape != "none":
            world_imgs["landscapes"] = landscape["imageUrls"]
            world_img["landscape"] = landscape = landscape["imageUrls"][0]
        else:
            world_img["landscape"], world_imgs["landscapes"] = "none", []
            
    else:
        landscape = world_img["landscape"] = "none"

    world.imgs = world_imgs
    world.save()
      
    locations = world.locations.filter(~Q(img__startswith="https"))
    locations_responses = []
    for i, location in enumerate(locations):
        print(f'working on {i+1}/{len(locations)} incomplete locations for {world.name}, world {world.id}')

        if isinstance(location.img, str) and not location.img == "none":
            try:
                location.img = upscale_img(location.img)
                base_url = img[-1:]
                location.imgs["thumbnails"] = [base_url + "0", base_url + "1", base_url + "2", base_url + "3"]
            except:
                location.img = "none"

        else:
            thumbnail = "none" if thumbnail is None else thumbnail
            landscape = "none" if landscape is None else landscape
            print (thumbnail + landscape)
            
            response = {}
            while not response.get("success", False):
                response = imagine(
                    {"model": "location", "id": location.id},
                    thumbnail + " " + landscape + " " +
                    ' '.join(world.genres) + " " + location.imagine + " --iw .42 --ar 3:4"
                )
                if response.get("success", False):
                    time.sleep(2)
            locations_responses.append(response)
    
    for i in range(len(locations_responses)):
        locations_responses[i] = wait_for_image(locations_responses[i])
            
    species_list = world.species.filter(~Q(img__startswith="https"))
    species_responses = []
    for i, speciez in enumerate(species_list):
        print(f'working on {i + 1}/{len(species_list)} incomplete species for {world.name}, world {world.id}')
        if isinstance(speciez.img, str) and not speciez.img == "none":
          try:
              speciez.img = upscale_img(speciez.img)
              base_url = img[-1:]
              speciez.imgs["thumbnails"] = [base_url + "0", base_url + "1", base_url + "2", base_url + "3"]
          except:
              speciez.img = "none"
      
        else:
            thumbnail = '' if thumbnail is None else thumbnail
            landscape = '' if landscape is None else landscape
            print (thumbnail + landscape)
        
            response = {}
            while not response.get("success", False):
                response = imagine(
                      {"model": "species", "id": speciez.id},
                      thumbnail + " " + landscape + " " +
                      ' '.join(world.genres) + " " + speciez.imagine + " --iw .55 --ar 3:4"
                  )
                if response.get("success", False):
                    time.sleep(2)
            
            species_responses.append(response)

    for i in range(len(species_responses)):
        species_responses[i] = wait_for_image(species_responses[i])

    chars = world.characters.filter(~Q(img__startswith="https"))

    for i, char in enumerate(chars):
        print(f'working on {i + 1}/{len(chars)} incomplete characters for {world.name}, world {world.id}')
        if isinstance(char.img, str) and not char.img == "none":
          try:
              img = char.img = upscale_img(char.img)
              base_url = img[-1:]
              char.imgs["thumbnails"] = [base_url + "0", base_url + "1", base_url + "2", base_url + "3"]
          except:
              char.img = "none"
        
        else:
            try:
                char_species = world.species.get(name=char.species)
            except Species.DoesNotExist:
                  try:
                      char_species = world.species.get(name=char.species[:-1])
                  except Species.DoesNotExist:
                      char_species = None

            if not char_species:
              char_species = world.species.order_by('?').first() 
            
            species_url = char_species.img if char_species else ''
            
            first_location = world.locations.order_by('?').first()
            location_url = first_location.img if first_location else ''

            response = {}
            while not response.get("success", False):
                response = imagine({"model": "character", "id": char.id}, 
                    location_url + " " + species_url + " " +
                    ' '.join(world.genres) + " " + char.imagine + " --iw .88 --ar 3:4")
                if response.get("success", False):
                  time.sleep(2) 

        if i == len(chars) - 1:
            wait_for_image(response)

    events = world.events.filter(~Q(img__startswith='https'))

    for i, event in enumerate(events):
        print(f'working on {i + 1}/{len(events)} incomplete events for {world.name}, world {world.id}')
        if isinstance(event.img, str) and not event.img == "none":
          try:
              img = event.img = upscale_img(event.img)
              base_url = img[-1:]
              event.imgs["thumbnails"] = [base_url + "0", base_url + "1", base_url + "2", base_url + "3"]
          except:
              event.img = "none"

        else:
            event_location = None

            try:
                event_location = world.locations.get(name=event.location)
            except Location.DoesNotExist:
                event_location = None

            response = {}
            location_url = event_location.img if event_location else world.locations.order_by('?').first().img

            while not response.get("success", False):
                response = imagine({"model": "event", "id": event.id}, 
                    location_url + " " + ' '.join(world.genres) + " " + event.imagine + " --iw .42 --ar 3:4")
                time.sleep(2)
            if i == len(events) - 1:
                wait_for_image(response)

    print('ding! world finished. wow!')



def wait_for_image(msg):
    if "messageId" in msg:
        try:
            update = get_progress(msg["messageId"])
        except:
            return 'none'

        progress = get_progress(msg["messageId"])["progress"]
        if isinstance(progress, str) and progress != 'incomplete':
            progress = int(progress)
            
        if progress < 10:
            print("job started, brb...")
            time.sleep(42)
            update = get_progress(msg["messageId"])

        while not update["progress"] == 100:
            print(f'hol\' up, job cookin\'.. {update["progress"]}%')
            time.sleep(4)
            update = get_progress(msg["messageId"])
            if update["progress"] == "incomplete":
                print('woops! job hanging, moving on..')
                return 'incomplete'

        print("ding! job finished.")
        return update["response"]
    

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


def update_all_images():
    worlds = World.objects.all()
    for i, world in enumerate(worlds):
        print(f'Working on {world.name}, world {world.id}, {i + 1} / {len(worlds)} worlds')
        add_midj_images(world)
    print("holy cow, that's all folks!!")


def generate_new_worlds(n=13):
    new_worlds = []
    for _ in range(n):
        try:
            new_world = generate_random_world()
            new_worlds.append(new_world)
        except Exception as e:
            print(f"Error generating new world: {e}")
    
    return new_worlds

generate_new_worlds(3)
