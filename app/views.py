from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import View
import base64
import os
import requests
import time


def image_create(prompt, image_name):
    engine_id = "stable-diffusion-xl-beta-v2-2-2"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    api_key = "sk-tYk6w9Fme97inuhtUIHXkbNlsrjQoI5GKjJWaN2qCHwmrWy3"

    # API Keyの取得確認
    if api_key is None:
        raise Exception("Missing Stability API key.")

    # API呼び出し
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
        },
    )

    # レスポンス確認
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    # レスポンス取得
    data = response.json()

    # 画像保存
    # ファイル名にはタイムスタンプとengine_id、通番を含めています
    # 通番は0〜samplesの値 - 1
    for i, image in enumerate(data["artifacts"]):
        with open(image_name, "wb") as f:
            f.write(base64.b64decode(image["base64"]))

class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'app/index.html')

    def post(self, request, *args, **kwargs):
        prompt = request.POST.get('prompt')
        image_name=f"static/img/{prompt}.png"

        print(image_name)
        image_create(prompt,image_name)

        # ここで画像の処理を実装する。例えば、画像名に基づいて画像を取得してHttpResponseを返す。
        # response = ...

        return render(request, 'app/index.html',{'image_name': image_name})

    def image_create(prompt,image_name):
        engine_id = "stable-diffusion-xl-beta-v2-2-2"
        api_host = os.getenv('API_HOST', 'https://api.stability.ai')
        api_key = "sk-tYk6w9Fme97inuhtUIHXkbNlsrjQoI5GKjJWaN2qCHwmrWy3"

        # API Keyの取得確認
        if api_key is None:
            raise Exception("Missing Stability API key.")

        # API呼び出し
        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": prompt
                    }
                ],
            },
        )

        # レスポンス確認
        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        # レスポンス取得
        data = response.json()

        # 画像保存
        # ファイル名にはタイムスタンプとengine_id、通番を含めています
        # 通番は0〜samplesの値 - 1
        for i, image in enumerate(data["artifacts"]):
            with open(image_name, "wb") as f:
                f.write(base64.b64decode(image["base64"]))