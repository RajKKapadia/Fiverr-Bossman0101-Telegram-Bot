import asyncio

import requests

import config


async def get_meshy_job_id(prompt: str) -> str:
    try:
        payload = {
            "mode": "preview",
            "prompt": prompt,
            "art_style": "realistic",
            "negative_prompt": "low quality, low resolution, low poly, ugly"
        }
        headers = {
            "Authorization": f"Bearer {config.MESHY_API_KEY}"
        }
        response = requests.post(
            "https://api.meshy.ai/v2/text-to-3d",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        response = response.json()
        return response["result"]
    except:
        return ""


async def retriev_meshy_job_by_id(task_id: str) -> tuple[list[str], list[str], list[str], bool]:
    headers = {
        "Authorization": f"Bearer {config.MESHY_API_KEY}"
    }
    flag = True
    status = False
    url = []
    video_url = []
    model_urls = []
    while flag:
        response = requests.get(
            f"https://api.meshy.ai/v2/text-to-3d/{task_id}",
            headers=headers,
        )
        response.raise_for_status()
        if response.status_code == 200:
            response = response.json()
            if response["status"] == "SUCCEEDED":
                url.append(response["thumbnail_url"])
                video_url.append(response["video_url"])
                model_urls.append(response["model_urls"])
                flag = False
                status = True
            if response["status"] == "FAILED":
                flag = False
                status = True
        await asyncio.sleep(1)
    return url, video_url, model_urls, status


async def call_meshy_api(prompt: str) -> tuple[list[str], list[str], list[str], bool]:
    task_id = await get_meshy_job_id(prompt=prompt)
    url = []
    video_url = []
    model_urls = []
    if task_id == "":
        return url, video_url, model_urls, False
    else:
        url, video_url, model_urls, status = await retriev_meshy_job_by_id(
            task_id=task_id)
        return url, video_url, model_urls, status
