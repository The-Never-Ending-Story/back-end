import json
from .api_services import gpt_response, dalle_image
from .prompts import gpt_prompt
# from worlds.models import World


def generate_world(params):
    world_response = gpt_response(gpt_prompt(params))

    try:
        world_json = json.loads(world_response)
        world_json["image"] = dalle_image(world_json["description"])

        return world_json
        #
        # world = World(**response_json)
        # world.save()

    except json.JSONDecodeError as e:
        error = f"""
        Error decoding JSON: {e}
        Response text: {response}"
        """
        return error


response = generate_world(
    {"geodynamics": "lush rainforest", "magicTechnology": {"magic": "true", "technological_level": "6"}})
print(response)
