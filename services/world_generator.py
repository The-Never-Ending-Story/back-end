import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worlds.settings")
django.setup()

import json
from .api_services import gpt_response, dalle_image, midjourney_image
from .prompts import gpt_prompt
from .attributes import AESTHETICS, GEODYNAMICS
import random
from worlds.models import World, Event, Location, Character, Species


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
        return world

    except json.JSONDecodeError as e:
        error = f"""
        Error decoding JSON: {e}
        Response text: {world_response}"
        """
        return error
    

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
    return random.sample(AESTHETICS[earthly], random.randint(1,4))


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
        "earthly": True,
        "genres": ["Highlandcore", "City Pop", "Elizabethan England"],
        "geoDynamics": {
            "size": "Earth-like",
            "shape": "Planet",
            "climate": "Tundra",
            "landscapes": ["Salt flats", "Rocky desert"]
        },
        "magicTechnology": {
            "magicLvl": 10,
            "magic": ["Elemental manipulation", "Time control", "Mind alteration", "Resurrection", "Realm traveling"],
            "techLvl": 4,
            "technology": ["Steampunk apparatus", "Elizabethan-era tools and machinery"]
        },
        "name": "HearthGlint",
        "blurb": "A timeless blend of gritty highland vistas and glimmering cityscapes, binding raw magical prowess with Elizabethan simplicity.",
        "description": "HearthGlint appears an odd fusion, a world of icy tundra and salt flats, interspersed with rocky deserts. The raw power of elemental magic courses through its veins, as steam-powered contraptions and Elizabethan-era technology elicit an oddly harmonious blend. Its population, though mostly formed of gritty Highlanders and cosmopolitan Urbians, also sees a strange race of salt-formed golems, shaped and given life by arcane forces. These peculiar contrasts make HearthGlint a place where the extraordinary is ordinary, and the mundane is mesmerizing.",
        "imagine": "Picture wide, crystalline salt flats under an unyielding sun, stretching out to the horizon as far as the eye can see till they blend with the icy tundra. Harsh, rocky cliffs tower over this scenery, keeping watch over the regal cities of gleaming spires veiled in enchanting aurora borealis, their cobblestone streets bustling with the morning market hype.",
        "species": [
            {
            "alignment": "Lawful good",
            "politics": "Monarchy",
            "name": "Highlander",
            "lore": "The Highlanders are a hearty race adapted to the harsh climates; they are stoically resilient, with an innate ability to manipulate rock and ice elements. Their society, steeped in honor and traditions, looks upon magic as the utmost profession.",
            "imagine": "Visualize a man wearing thick, woolen cloaks, his armored boots resonating against cobblestones. His gaze, as steady and unyielding as the mountain he hails from, holds an unspoken promise of duty and protection."
            },
            {
            "alignment": "Neutral",
            "politics": "Trade Republic",
            "name": "Urbian",
            "lore": "The Urbians are a sophisticated breed, clever manipulators of elemental forces to create mesmerizing illusions and extravagant living conditions. Urbians play pivotal roles in the economic gears of HearthGlint, their society thriving on commerce and innovation.",
            "imagine": "Imagine a lady dressed in rich velvets and ruffs, an aura of finesse about her. An array of elements dance upon her fingertips, as she arranges them into a magnificent illusion, mimicking the Aurora Borealis."
            },
            {
            "alignment": "True neutral",
            "politics": "Anarchy",
            "name": "Saline Golem",
            "lore": "",
            "imagine": "Glimpse a statueque creature of glistening salt crystals, its form shimmering under the sun, as it treks solemnly across the salt plains. Curiously aware, it feels the pulse of magic within it, the very essence of its existence."
            }
        ],
        "locations": [
            {
            "type": "City",
            "climate": "Cold",
            "name": "Iceglen",
            "lore": "Iceglen, the capital of the Highlanders, boasts towering ice-sculpted buildings set against the stark, icy tundra. Its beating heart lies in its grand castle, sculpted purely of magic-hardened ice.",
            "imagine": "See a cityscape adorned with towering ice structures, illuminated from within, casting an ethereal glow under the twilight. The grand castle, the labor of magic, stands as a breathtaking masterpiece amidst the glittering snowscape."
            },
            {
            "type": "City",
            "climate": "Mild",
            "name": "Mirage",
            "lore": "Mirage, the Urbian city, is an architectural marvel. The illusion magic that the Urbians wield make the buildings shimmer in the day and glow at night, resulting in a continuous play of light and shadow.",
            "imagine": "Envision a city sparkling with magic-induced iridescence, its architecture morphing in a dance of illusion. As daylight wanes, the city glows from within, casting its kaleidoscopic brilliance across the cloud-strewn twilight."
            }
        ],
        "characters": [
            {
            "species": "Highlander",
            "age": 38,
            "alignment": "Lawful good",
            "name": "Thorgal Frostborn",
            "lore": "Thorgal is a respected platoon leader in Iceglen, known for his stoic resilience and brilliant tactical mind. He played a crucial role in the great Battle of the Shattered Peaks.",
            "imagine": "Picture a hardened warrior standing against the backdrop of a frozen landscape. His breath freezes in the cold as he looks upon a towering fortress of icy stalagmites, a silent vow etched in his gaze."
            },
            {
            "species": "Urbian",
            "age": 32,
            "alignment": "Neutral",
            "name": "Elyra Starlight",
            "lore": "Elyra is a renowned Illusion Mage of Mirage, famed for her artistry and creative vision. Her illusions during the annual Festival of Lights are the city's most anticipated event.",
            "imagine": "Visualize a lady emanating an otherworldly charisma, her eyes sparkling with magic, as colorful lights dance in the dusk, mirroring the starlit sky in her creation."
            }
        ],
        "events": [
            {
            "type": "Battle",
            "age": "The age of Discord",
            "time": 1562,
            "name": "Battle of the Shattered Peaks",
            "lore": "Led by Thorgal, the Highlanders withstood the onslaught of invading Saline Golems in the icy Shattered Peaks. The Battle culminated in a magical explosion that rendered the Golems inert, securing the Highlander victory.",
            "imagine": "Visualize warring factions amidst snow-laden peaks under stormy skies. Elemental energy crackles in the tense air as combatants clash, the ensuing explosion illuminates the icy battlefield."
            },
            {
            "type": "Festival",
            "age": "The age of Harmony",
            "time": 1597,
            "name": "Festival of Lights",
            "lore": "The Urbians annually celebrate the Festival of Lights, where illusion magic is used to fill the city with wondrous sights. Elyra's spectacle during the Festival brought both Highlanders and Urbians together, facilitating unity.",
            "imagine": "Imagine the city under a cascade of scintillating lights, born of magic, painting the dusk with splashes of crimson and gold, deepening the sense of communal camaraderie."
            }
        ],
        "lore": [
            "During the Age of Discord, HearthGlint was a land divided. The Highlanders and Urbians, disparate in their lifestyle, dealt with each other through shrewd politics and commerce. The Saline Golems, born out of the very lifeblood of the land, were seen as naturally destructive entities not conforming to societal norms.",
            "The Age of Battle marked a turning point in the story of HearthGlint. The battle of Shattered Peaks between Highlanders and golems ended in a magical explosion, rendering the golems dormant. This event marked an era of coexistence, leading to closer ties among Highlanders and Urbians, and an understanding that Golems were sentient beings to be respected.",
            "The Age of Harmony saw the blending of magic and technology reach its pinnacle. The Festival of Lights, yearly celebrated by Urbians, played a significant role in establishing this harmony, making HearthGlint a world where magic isn't just a tool, but a thread that binds its inhabitants in a communal brotherhood."
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