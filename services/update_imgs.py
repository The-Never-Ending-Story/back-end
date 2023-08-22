from .world_generator import update_all_images
import os
from PIL import Image
from io import BytesIO
from worlds.models import World
import base64
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .api_services import imagine
from .world_generator import wait_for_image

def compress_thumbnail(world):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    
    # Instantiate the driver inside the function
    driver = webdriver.Chrome(options=chrome_options)

    try:
        print(f"---\nStarting world {world.id}")
        pattern = re.compile(r"\.png$") 
        thumbnail_url = world.img.get("thumbnail")
        
        if not thumbnail_url:
            print(f"No thumbnail URL for world {world.id}")

        print(f"Thumbnail URL: {thumbnail_url}")
        
        if not pattern.search(thumbnail_url):
            print(f"URL doesn't match the pattern: {thumbnail_url}")
        
        # Navigate to the URL using Selenium
        driver.get(thumbnail_url)
        
        # Sleep to ensure page loads and any challenges are handled
        time.sleep(5)
        
        # Capture the screenshot as the image
        img_data = driver.get_screenshot_as_png()
        
        print(f"Successfully fetched image for world {world.id}")

        img = Image.open(BytesIO(img_data))
        img.thumbnail((200, 200))

        compressed_img_data = BytesIO()
        img.save(compressed_img_data, format='PNG', quality=95)
        base64_encoded = base64.b64encode(compressed_img_data.getvalue()).decode('utf-8')
        world.img["thumbnail"] = base64_encoded
      
        print(f"Compressed image for world {world.id}")
        
        world.save()
        print(f"Saved world {world.id}")

    except Exception as e:
        print(f"Error for world {world.id} while accessing URL {thumbnail_url}. Error: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed after each usage.

def compress_thumbnails():
    worlds = World.objects.all()

    for world in worlds:
        compress_thumbnail(world)


def get_new_heros():
    worlds = World.objects.all()

    for world in worlds:
      print(f'working on hero for world {world.id}...')

      thumbnail = world.imgs.get("thumbnails")
      if thumbnail:
          thumbnail = thumbnail[0]

      pattern = re.compile(r"\.png$") 

      if thumbnail and pattern.search(thumbnail):

        hero = {}
        while not hero.get("success", False):
            hero = imagine(
            {"model": "world", "id": world.id, "type": "hero"},
            thumbnail + " " + ' '.join(world.genres) + " " + world.imagine + " --iw .75 --ar 3:2"
            )
            if hero.get("success") == False:
                time.sleep(3)

        hero = wait_for_image(hero)
        print(f"hero finished for world {world.id}")
      
      else: 
          print("world is missing thumbnail")
      

get_new_heros()

# compress_thumbnails()

# update_all_images()