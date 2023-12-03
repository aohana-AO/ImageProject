from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.views.generic import View
import base64
import os
import requests
import time
import environ
from .models import Image


def image_create(prompt, negative_prompt, image_name):
    engine_id = "stable-diffusion-xl-1024-v1-0"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    env = environ.Env()
    api_keys = env('IMAGE_API_KEY').split(',')

    current_api_key_index = 0  # 現在のAPIキーのインデックス
    Style_preset = ["3d-model", "analog-film", "anime", "cinematic", "comic-book", "digital-art", "enhance",
                    "fantasy-art", "isometric", "line-art", "low-poly", "modeling-compound", "neon-punk", "origami",
                    "photographic", "pixel-art", "tile-texture"]
    while current_api_key_index < len(api_keys):
        # API Keyの取得確認
        if api_keys[current_api_key_index] is None:
            raise Exception("Missing Stability API key.")
        current_api_key = api_keys[current_api_key_index]
        # API呼び出し
        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {current_api_key}"
            },
            json={
                # "Samples": 1,画像生成枚数の指定
                # "style_preset": Style_preset[6],
                "text_prompts": [
                    {
                        "text": prompt
                    },
                    {
                        "text": negative_prompt,
                        "weight": -1.0
                    }
                ],
            },
        )
        # レスポンス確認
        if response.status_code == 200:
            break  # APIキーが有効な場合はループを抜けます
        elif response.status_code == 429:
            # APIキーが無効な場合、次のAPIキーに切り替えます
            current_api_key_index += 1
        else:
            raise Exception("Non-200 response: " + response.status_code + str(response.text))

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
        Images = Image.objects.filter(user_ID=self.request.user)
        return render(request, 'app/index.html', {'Images': Images})

    def post(self, request, *args, **kwargs):
        prompt = request.POST.get('prompt')
        negative_prompt = request.POST.get('negative_prompt')
        image_name = f"img/{prompt}_{negative_prompt}.png"

        print(image_name)
        image_create(prompt, negative_prompt, f'static/{image_name}')

        Image.objects.create(
            user_ID=self.request.user,
            image_path=image_name,
            prompt=prompt,
            negative_prompt=negative_prompt
        )

        Images = Image.objects.filter(user_ID=self.request.user)

        return render(request, 'app/index.html', {'image_name': image_name, 'Images': Images})


def image_detail_view(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    Images = Image.objects.filter(user_ID=request.user)
    return render(request, 'app/index.html', {'image': image, 'Images': Images})
