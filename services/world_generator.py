import json
from .api_services import gpt_response, midjourney_image
from .prompts import gpt_prompt
# from worlds.models import World


def generate_world(params):
    world_response = gpt_response(gpt_prompt(params))

    try:
        world_json = json.loads(world_response)
        world_json["image"] = midjourney_image(world_json["imagine"])

        return world_json

        # world = World(**world_json)
        # world.save()
        #
        # return world

    except json.JSONDecodeError as e:
        error = f"""
        Error decoding JSON: {e}
        Response text: {response}"
        """
        return error


response = generate_world(
    {"magicTechnology": {"magic": "true", "technological_level": "6"}, "genres": ["vaporwave", "fantasy"]})
print(response)
