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

def compress_thumbnail(world):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    
    # Instantiate the driver inside the function
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

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

compress_thumbnails()

# update_all_images()