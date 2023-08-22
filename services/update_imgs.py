from .world_generator import update_all_images
import requests
from PIL import Image
from io import BytesIO
from worlds.models import World
import base64
import re

def compress_thumbnail(world):
    try:
        print(f"---\nStarting world {world.id}")
        pattern = re.compile(r"\.png$") 
        thumbnail_url = world.img.get("thumbnail")
        
        if not thumbnail_url:
            print(f"No thumbnail URL for world {world.id}")

        print(f"Thumbnail URL: {thumbnail_url}")
        
        if not pattern.search(thumbnail_url):
            print(f"URL doesn't match the pattern: {thumbnail_url}")
        
        # disguise our script as a regular browser to avoid 403 client forbidden
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Upgrade-Insecure-Requests": "1"
        }

        cookies = {
            "_ga": "GA1.1.1964539518.1677658582",
            "cf_clearance": "BCp.e70szH7kJb5u6FdkBznCAktadbKiV_TwQZCDrxw-1689526124-0-250",
            "_ga_Q0DQ5L7K0D": "GS1.1.1689526139.57.0.1689526142.0.0.0",
            "__cf_bm": "3yk.VOewZS9O_oW.GdTlcORS.1xxItG3O0WxRIwkHZY-1692733255-0-AR/HOEsOxPYbvBelziq8xgZUN1nPyIcahHIGbrClE/ylGlYkG+5bvZvftawjtvangq2B7hSk/yWauvP+BX0M8tM="
        }

        response = requests.get(thumbnail_url, headers=headers, cookies=cookies)
        
        response.raise_for_status()  # raise exception for HTTP errors
        
        print(f"Successfully fetched image for world {world.id}")
        
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img.thumbnail((200, 200))

        compressed_img_data = BytesIO()
        img.save(compressed_img_data, format='PNG', quality=95)
        base64_encoded = base64.b64encode(compressed_img_data.getvalue()).decode('utf-8')
        world.img["thumbnail"] = base64_encoded
      
        print(f"Compressed image for world {world.id}")
        
        world.save()
        print(f"Saved world {world.id}")

    except requests.RequestException as e:
        print(f"Error fetching image for world {world.id} from URL {thumbnail_url}. Error: {e}")
    except Exception as e:
        print(f"Unknown error for world {world.id}. Error: {e}")

def compress_thumbnails():
    worlds = World.objects.all()

    for world in worlds:
        compress_thumbnail(world)

compress_thumbnails()

# update_all_images()