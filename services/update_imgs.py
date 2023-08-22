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
      print(f"working on world {world.id}")
      thumbnail_url = world.img.get("thumbnail")
      if thumbnail_url and pattern.search(thumbnail_url):
          response = requests.get(thumbnail_url)
          
          if response.status_code == 200:
              print("image fetched")
              img_data = response.content
              img = Image.open(BytesIO(img_data))
              img.thumbnail((200, 200))

              compressed_img_data = BytesIO()
              img.save(compressed_img_data, format='PNG', quality=95)


              world.thumbnail = compressed_img_data.getvalue()
              print("image compressed")
              world.save()
          else:
              print(f"Failed to fetch image: {thumbnail_url}")


compress_thumbnails()
# update_all_images()