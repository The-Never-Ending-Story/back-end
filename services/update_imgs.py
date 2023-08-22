from .world_generator import update_all_images
import requests
from PIL import Image
from io import BytesIO
from worlds.models import World
import re

def compress_thumbnails():
    worlds = World.objects.all()
    pattern = re.compile(r"\.png$")

    for world in worlds:
        try:
            print(f"---\nStarting world {world.id}")
            thumbnail_url = world.img.get("thumbnail")
            
            if not thumbnail_url:
                print(f"No thumbnail URL for world {world.id}")
                continue

            print(f"Thumbnail URL: {thumbnail_url}")
            
            if not pattern.search(thumbnail_url):
                print(f"URL doesn't match the pattern: {thumbnail_url}")
                continue

            response = requests.get(thumbnail_url)
            
            response.raise_for_status()  # raise exception for HTTP errors
            
            print(f"Successfully fetched image for world {world.id}")
            
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img.thumbnail((200, 200))

            compressed_img_data = BytesIO()
            img.save(compressed_img_data, format='PNG', quality=95)
            
            world.img["thumbnail"] = compressed_img_data.getvalue()
            print(f"Compressed image for world {world.id}")
            
            world.save()
            print(f"Saved world {world.id}")

        except requests.RequestException as e:
            print(f"Error fetching image for world {world.id} from URL {thumbnail_url}. Error: {e}")
        except Exception as e:
            print(f"Unknown error for world {world.id}. Error: {e}")

compress_thumbnails()

# update_all_images()