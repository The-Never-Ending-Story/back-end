import requests
import json
import openai
from prompts import gpt_prompt
from settings import OPENAI_API_KEY


def get_gpt_response(prompt):
    openai.api_key = OPENAI_API_KEY
    messages = [{"role": "system", "content": "You are an API endpoint. Please respond as a JSON field"},
                {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1.0,
        max_tokens=3690,
        n=1,
        stop=None,
    )
    return response.choices[0].message.content.strip()


def generate_dalle_image(prompt):
    openai.api_key = OPENAI_API_KEY
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url


def generate_midjourney_image(prompt):
    url = "https://api.thenextleg.io/v2/imagine"

    payload = json.dumps({
        "msg": prompt,
        "ref": "",
        "webhookOverride": ""
    })
    headers = {
        'Authorization': 'Bearer <your-token>',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def generate_world(params):
    response = get_gpt_response(gpt_prompt(params))
    try:
        response_json = json.loads(response)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response text: {response}")
    image_instructions = "A landscape view of the following world: " + response_json["description"]
    response_json["image"] = generate_dalle_image(image_instructions)

    return response_json


response = generate_world(
    {"geodynamics": "lush rainforest", "magicTechnology": {"magic": "true", "technological_level": "6"}})
print(response)
