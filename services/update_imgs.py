from .world_generator import update_all_images
import requests
from PIL import Image
from io import BytesIO
from worlds.models import World
import re

def compress_thumbnails():
  worlds = World.objects.all()  

  for world in worlds:
      pattern = re.compile(r"\.png$")
      thumbnail_url = world.img.get("thumbnail")
      if thumbnail_url and pattern.search(thumbnail_url):
        response = requests.get(thumbnail_url)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img.thumbnail((200, 200))

        compressed_img_data = BytesIO()
        img.save(compressed_img_data, format='PNG', quality=95)  

        world.thumbnail = compressed_img_data.getvalue()
        world.save()

compress_thumbnails()
# update_all_images()