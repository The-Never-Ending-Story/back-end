import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worlds.settings")
django.setup()

import json
from .api_services import gpt_response, dalle_image, imagine, upscale_img
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
        add_midj_images(world)
        return world

    except json.JSONDecodeError as e:
        error = f"""
        Error decoding JSON: {e}
        Response text: {world_response}"
        """
        return error
    
def add_midj_images(world):
        response = imagine({"model": "world", "id": world.id, "type": "thumbnail"}, ' '.join(world.genres) + " " + world.description)
        print(response)
        wait_for_image(world, "thumbnail")
        world.img["thumbnail"] = upscale_img(world.img["thumbnail"])
        world.save()
        
        imagine({"model": "world", "id": world.id, "type": "landscape"}, world.img["thumbnail"] + " " + ' '.join(world.genres) + " " + world.imagine + " --ar 9:3")
        wait_for_image(world, "landscape")
        world.img["landscape"] = upscale_img(world.img["landscape"])
        world.save()

        for location in world.locations.all():
            response = imagine({"model": "location", "id": location.id}, world.img["thumbnail"] + " " + ' '.join(world.genres) + " " + location.imagine + " --ar 3:4")
            print(response)
            wait_for_image(location)
            location.img = upscale_img(location.img)
            location.save()
            
        for species in world.species.all():
            imagine({"model": "species", "id": species.id}, world.img["thumbnail"] + " " + ' '.join(world.genres) + " " + species.imagine + " --ar 3:4")
            wait_for_image(species.img)
            species.img = upscale_img(species.img)
            species.save()

            for char in world.characters.filter(species=species):
                imagine({"model": "character", "id": char.id}, world.img["thumbnail"] + " " + species.img + " " + char.imagine + " --ar 3:4")
                wait_for_image(char.img)
                char.img = upscale_img(char.img)
                char.save()

        for event in world.events.all():
            imagine({"model": "event", "id": event.id}, world.img["thumbnail"] + " " + event.imagine + " --ar 3:4")
            wait_for_image(event.img)
            event.save()
        
        return world

def wait_for_image(instance, type=False):
    time.sleep(30)
    if type:
        while not instance.img.get(type):
            instance.refresh_from_db()
            print(instance.img)
            print("waiting...")
            time.sleep(5)
    else:
        while (not instance.img or instance.img == "none"):
            instance.refresh_from_db()
            print(instance.img)
            print("waiting...")
            time.sleep(5)
    

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







def generate_this_world():
    world_json = {
  "name": "Abyssia",
  "earthly": true,
  "genres": ["Pre-Raphaelite", "Art Nouveau", "Forestpunk"],
  "img": {
    "landscape": "https://cdn.discordapp.com/attachments/1128814452012220536/1129471815505424465/hyperloom_Abyssia_is_a_world_tucked_away_within_its_aquamarine__3c94e2c0-790f-4226-881b-1e06dbbc9a5e.png",
    "thumbnail": "https://cdn.discordapp.com/attachments/1128814452012220536/1129470452780245012/hyperloom_Stepping_ashore_you_find_yourself_encased_in_perpetua_513849bf-0aa4-4b0d-9078-61129fcae8b3.png"
  },
  "geoDynamics": {
    "size": "Dwarf",
    "shape": "Planet",
    "climate": "oceanic",
    "landscapes": ["plateaus", "taiga"]
  },
  "magicTechnology": {
    "magicLvl": 6,
    "magic": {
      "Chaos": "Alteration of reality",
      "Nature": "Manipulation of plants and animals",
      "Element": "Control over fire, water, earth and air"
    }, 
    "techLvl": 8,
    "technology": {
      "BioTech": "Genetic modifications",
      "Inventions": "Steam-powered machines",
      "InfoTech": "Centralized information network"
    }
  },
  "blurb": "Sea-lapped enigma draped in verdure and shrouded in mystery.",
  "description": "Abyssia is a world tucked away within its aquamarine oceanic veil, bejeweled with islands of varying sizes and forestry. The gaps between these isles allow space for the expansive teeming marine life, keeping the Abyssian archipelago alive. The exquisite landscapes are concoctions of towering plateaus, silhouetted against twilight, and dense taiga forests, a testament to the potent magic that enhances the verdant vibrancy. The age of steam powers the Abyssian's inventions while they still invoke nature, element, and chaos magics.",
  "imagine": "Stepping ashore, you find yourself encased in perpetual dawn. Majestic plateau peaks are bathed in orange light, their bare rock faces contrasting with rich verdant taiga at their base. Twisted boughs of ancient trees disappear into an emerald canopy pierced by whimsical shafts of sunlight, while curious steam contraptions whirr away on their predestined tasks. As dusk sets, you see the sparkling ocean stretch far beyond, while thousands of bioluminescent creatures awaken, setting the world aglow.",
  "species": [{
    "alignment": "Neutral Good",
    "politics": "Matriarchal society",
    "name": "Abythonians",
    "lore": "Being amphibious in nature, Abythonians harmonize their life between land and sea. They are adept in harnessing both magic and technology to enhance their survival. Their society is led by the Matriarch, an individual known for her superior knowledge of both the land and marine ecosystems.",
    "imagine": "In the interplay of light, amidst a tangle of branches, figures move with fluid grace. Their elongated limbs, covered in scales glistening in various hues, prove to be as functional in land as they are in water. A unique bioluminescent mark, glowing at the center of their forehead, seems to pulsate with every beat of their heart. Walking by you, they interact with a curious steam contraption that nests amidst the trees, their eyes reflecting unspoken wisdom.",
    "img": "https://cdn.discordapp.com/attachments/1128814452012220536/1129483134682017912/hyperloom_Being_amphibious_in_nature_Abythonians_harmonize_thei_0a6ebdbe-0ecd-437a-84f4-d79ef759df6a.png" }],
  "locations": [{
    "type": "City",
    "climate": "Temperate rainforest",
    "name": "Arbores Altum",
    "lore": "Arbores Altum, the city built amidst the treetops, demonstrates a remarkable integration of nature. Houses wrapped in flora rely on steam-powered lifts for mobility. It's a pre-Raphaelite vision infused with the animation of forestpunk.",
    "imagine": "Gaze upwards at a city thriving amidst the canopy. Platforms wrapped in tapestry of foliage, steam powered lifts bustling with activity, weaving their way between the branches. Soft twinkle of bioluminescent plants light the city with a dreamy glow, reflecting off the waterproofed canvases stretched over their fortifications.",
    "img": "https://cdn.discordapp.com/attachments/1128814452012220536/1129483528845934682/hyperloom_Gaze_upwards_at_a_city_thriving_amidst_the_canopy._Pl_863e563d-6a6f-46e7-9400-0e58e300adaa.png" }],
  "characters": [{
    "species": "Abythonians",
    "age": 127,
    "alignment": "Neutral Good",
    "name": "Nymphaea",
    "lore": "Nymphaea, the current Matriarch of the Abythonians, is known for her serene wisdom, potent magic skills, and deep connection with nature. She played a pivotal role in the creation of the Abyssian Information Network.",
    "imagine": "Lingering gaze of a serene figure, enchanting everyone around her. Her iridescent scales glow dimly, a symbol of her mature age. Adroit fingers engage in a magical dance, drawing energy from the atmosphere, while before her a whirl of steam forms intricate patterns, symbolizing her contribution to the fusion of magic and technology.",
    "img": "https://cdn.discordapp.com/attachments/1128814452012220536/1129484262329028638/hyperloom_Lingering_gaze_of_a_serene_figure_enchanting_everyone_8215101d-2efd-4ef9-a45d-80022f6e5c8b.png" }],
  "events": [{
    "type": "Peace Treaty",
    "age": "Third Age",
    "time": "TA 37",
    "name": "The Pact of Coexistence",
    "lore": "This pact marked the end of the wars amongst the Abyssian sub-species. The treaty emphasized on mutual survival, marking the birth of the Union of Abyssia.",
    "imagine": "Picture the twilight-soaked plateau, where two figures stand against each other. Their palms glow with magical symbols, indicating their binding oath. Around them gather their kin, awestruck as the spectacle of harmony unfolds before the setting sun.",
    "img": "https://cdn.discordapp.com/attachments/1128814452012220536/1129484637786341427/hyperloom_Picture_the_twilight-soaked_plateau_where_two_figures_58fa4aa5-8cc3-4989-ac28-c84bde24b488.png" }],
    "lore": [
    "Era of Emergence: The first epoch marks the rise of the Abythonians. Fierce competition for resources led to the discovery of magic and technology, intertwining the society into a web of politics and power struggles. The Abythonians soon learned to adapt and carve out territories within their confines.",
    
    "Age of Enlightenment: During the second epoch, the Abythonians embraced their magic-technology blend. This age saw the construction of the city Arbores Altum and the blossoming of knowledge, with the invention of the Abyssian Information Network. Under Nymphaea's leadership, the Abythonians explored the depths of their abilities, found balance with the environment, and sparked rapid progress and growth.",
    
    "The Union Age: Brought about by the Pact of Coexistence, the third epoque marked the end of internal conflict between the Abythonians. The epoch ushered in an era of peace, harmony, and shared survival amongst the Abyssian sub-species."
  ]
}

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

        return world

    
world = generate_random_world()
print(world)

# img = midjourney_image("a wormhole to another dimension")
# print(img)