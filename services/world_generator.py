import json
from api_services import gpt_response, generate_dalle_image
from prompts import gpt_prompt


def generate_world(params):
    response = gpt_response(gpt_prompt(params))
    try:
        response_json = json.loads(response)
        image_instructions = "A landscape view of the following world: " + response_json["description"]
        response_json["image"] = generate_dalle_image(image_instructions)

        return response_json

    except json.JSONDecodeError as e:
        error = f"""
        Error decoding JSON: {e}
        Response text: {response}"
        """
        return error


response = generate_world(
    {"geodynamics": "lush rainforest", "magicTechnology": {"magic": "true", "technological_level": "6"}})
print(response)
