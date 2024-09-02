import time
import requests
import base64
from typing import List, Any, Dict, Tuple
import json

import config


auth_header = "Basic " + base64.b64encode(
    f"{config.SCENARIO_API_KEY}:{config.SCENARIO_SECRET_KEY}".encode('ascii')).decode('ascii')


base_url = 'https://api.cloud.scenario.com/v1'
model_id = 'NKStdSjYQjaeFiTK9ps8dg'

headers = {
    'accept': 'application/json',
    'Authorization': auth_header
}


def extract_image_urls(inference_data: dict[str, any]) -> Tuple[List[str], List[str]]:
    images = inference_data.get('inference', {}).get('images', [])
    urls = []
    image_ids = []
    for image in images:
        urls.append(image["url"])
        image_ids.append(image["id"])
    return urls, image_ids


def remove_background(image_id: str) -> str:
    url = f"{base_url}/generate/remove-background"
    payload = {"image": image_id,
               "backgroundColor": "#ffffff"}
    response = requests.post(url, json=payload, headers=headers)
    response = dict(json.loads(response.text))
    url = response.get("asset", {}).get("url", "")
    return url


def call_scenario_api(prompt: str) -> Dict[str, Any]:
    response = requests.post(
        url=f'{base_url}/generate/txt2img',
        json={
            'modelId': model_id,
            'prompt': prompt + "image must have transparent background",
            'numInferenceSteps': 30,
            'numSamples': 2,
            'guidance': 7.5,
            'width': 1024,
            'height': 1024,
            "originalAssets": True
        },
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        inference_id = data['inference']['id']
        status = ''
        while status not in ['succeeded', 'failed']:
            inference_response = requests.get(
                f'{base_url}/models/{model_id}/inferences/{inference_id}', headers=headers)
            inference_data = dict(inference_response.json())
            status = inference_data['inference']['status']
            time.sleep(5)
        if status == 'succeeded':
            _, image_ids = extract_image_urls(inference_data=inference_data)
            urls = []
            for image_id in image_ids:
                url = remove_background(image_id=image_id)
                urls.append(url)
            return {
                "status": True,
                "urls": urls
            }
        else:
            return {
                "status": False,
                "urls": []
            }
    else:
        return {
            "status": False,
            "urls": []
        }
