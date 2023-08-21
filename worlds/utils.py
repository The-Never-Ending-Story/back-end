import random
from worlds.models import World

GENRE_MAPPING = {
    'Historical & Cultural': [
        '1950s Suburbia', 'American Pioneers', 'American Revolution', 'Americana', 
        'Ancient Egypt', 'Art Deco', 'Art Nouveau', 'Australian Outback', 'Baroque', 
        'Bauhaus', 'Classicism', 'Danish Pastel', 'Elizabethan England', 'Gothic', 
        'Impressionism', 'Italian Renaissance', 'Medieval', 'Neoclassicism', 
        'Neo-Romanism', 'Old Hollywood', 'Pre-Raphaelite', 'Romanticism', 'Victorian', 
        'World War II'
    ],
    'Nature & Environment': [
        'Autumn', 'Beach Day', 'Cabincore', 'Cottagecore', 'Desertwave', 'Earthcore', 
        'Forestpunk', 'Gardencore', 'Golden Hour', 'Grasscore', 'Highlandcore', 
        'Junglecore', 'Naturecore', 'Ocean Academia', 'Ocean Grunge', 'Rusticcore', 
        'Swampcore'
    ],
    'Urban & Modern': [
        'Abstract Tech', 'Atompunk', 'City Pop', 'Cyberprep', 'Decopunk', 'Diner', 
        'Miami Metro', 'Midwest Gothic', 'Minimalism', 'Nuclear', 'Suburban', 'Vintage'
    ],
    'Fantasy & Mystical': [
        'Alien', 'Dark Fantasy', 'Ethereal', 'Fairy Tale', 'Fantasy', 'Medieval Fantasy', 
        'Surrealism'
    ],
    'Futuristic & Tech': [
        'Afrofuturism', 'Clockpunk', 'Cyberdelic', 'Cyberpunk', 'Futurism', 'Gadgetpunk', 
        'Icepunk', 'Retro-Futurism', 'Silkpunk', 'Spacecore', 'Steampunk', 'Transhumanism', 
        'Underwater', 'Utopiacore', 'Wavepunk', 'Woodpunk'
    ],
    'Miscellaneous & Niche': [
        'Auroracore', 'Goblincore', 'Military', 'Monumentality', 'Mushroomcore', 'Nautical', 
        'New England Gothic', 'Paleocore', 'Pirate', 'Post-Apocalyptic', 'Prehistoricore', 
        'Sandalpunk', 'Seapunk', 'Stonecore'
    ]
}

def get_category_based_on_genre(genre):
    for category, genres_list in CATEGORY_MAPPING.items():
        if genre in genres_list:
            return category
    return None

def assign_category_to_world(world):
    category_counts = {}

    for genre in world.genres:
        category = get_category_based_on_genre(genre)
        if category:
            category_counts[category] = category_counts.get(category, 0) + 1

    sorted_categories = sorted(
        category_counts.keys(),
        key=lambda category: (
            category_counts[category], 
            -World.objects.filter(categories=category).count()
        ),
        reverse=True
    )

    if len(sorted_categories) > 1 and category_counts[sorted_categories[0]] == category_counts[sorted_categories[1]]:
        return random.choice(sorted_categories)
    
    return sorted_categories[0]

def assign_categories_to_worlds():
    worlds = World.objects.all()

    for world in worlds:
        world.categories = [assign_category_to_world(world)]
        world.save()
