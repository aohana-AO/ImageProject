from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
import base64
import os
import requests
import time
import environ
from .models import Image

def image_create(prompt, negative_prompt=None, image_name=None, number=None):
    engine_id = "stable-diffusion-xl-1024-v1-0"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    env = environ.Env()
    api_keys = env('IMAGE_API_KEY').split(',')

    number = int(number) if number is not None else None
    current_api_key_index = 0  # 現在のAPIキーのインデックス​
    Style_preset = ["3d-model", "analog-film", "anime", "cinematic", "comic-book", "digital-art", "enhance",
                    "fantasy-art", "isometric", "line-art", "low-poly", "modeling-compound", "neon-punk", "origami",
                    "photographic", "pixel-art", "tile-texture"]

    while current_api_key_index < len(api_keys):
        # APIキーの取得確認
        if api_keys[current_api_key_index] is None:
            raise Exception("Stability APIキーが見つかりません。")
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
                # 画像生成のサンプル数を指定
                "style_preset": Style_preset[number-1],
                "text_prompts": [
                    {
                        "text": prompt
                    },
                    {
                        "text": negative_prompt,
                        "weight": -1.0
                    } if negative_prompt else {}
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
            if "credits" in response.text and int(response.json()["credits"]) == 0:
                raise Exception("Your credits are depleted. Please refill your credits.")
            else:
                raise Exception("Non-200 response: " + str(response.status_code) + str(response.text))​
    # レスポンス取得
    data = response.json()

    # 画像保存
    # ファイル名にはタイムスタンプとengine_id、通番を含めています
    # 通番は0〜samplesの値 - 1
    # 
    # 
    if image_name and data.get("artifacts"):
        for i, image in enumerate(data["artifacts"]):
            with open(image_name, "wb") as f:
                f.write(base64.b64decode(image["base64"]))

class IndexView(View):
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return render(request, 'app/index.html')
        else:
            Images = Image.objects.filter(user_ID=self.request.user)
            return render(request, 'app/index.html', {'Images': Images})

    def post(self, request, *args, **kwargs):
        prompt = request.POST.get('prompt')
        negative_prompt = request.POST.get('negative_prompt')
        image_name = f"img/{prompt}_{negative_prompt}.png"
        number = request.POST.get('number')
        print(number)
        print(image_name)
        # numberパラメータをimage_create関数に渡す
        image_create(prompt, negative_prompt, f'static/{image_name}', number)​
        Image.objects.create(
            user_ID=self.request.user,
            image_path=image_name,
            prompt=prompt,
            negative_prompt=negative_prompt,
            ##selected_number=number
        )

        Images = Image.objects.filter(user_ID=self.request.user)​
        return render(request, 'app/index.html', {'image_name': image_name, 'Images': Images, 'number': number})

def image_detail_view(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    Images = Image.objects.filter(user_ID=request.user)
    return render(request, 'app/index.html', {'image': image, 'Images': Images})

def image_gallery_view(request):
    Images = Image.objects.filter(user_ID=request.user)
    return render(request, 'app/gallery.html', {'Images': Images})















