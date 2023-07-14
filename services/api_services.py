import requests
import json
import openai
from .settings import OPENAI_API_KEY
from .settings import MIDJ_API_KEY


def gpt_response(prompt):
    openai.api_key = OPENAI_API_KEY
    messages = [{"role": "system", "content": "You are an API endpoint. Please respond as a JSON field"},
                {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1.0,
        max_tokens=3000,
        n=1,
        stop=None,
    )
    return response.choices[0].message.content.strip()


def dalle_image(prompt):
    openai.api_key = OPENAI_API_KEY
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url


def midjourney_image(prompt):
    url = "https://api.thenextleg.io/v2/imagine"

    payload = json.dumps({
        "msg": prompt,
        "ref": "",
        "webhookOverride": "",
        "ignorePrefilter": "false"
    })
    headers = {
        'Authorization': f'Bearer {MIDJ_API_KEY}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text