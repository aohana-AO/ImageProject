from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import View
import base64
import os
import requests
import time
import environ

def image_create(prompt, image_name):
    engine_id = "stable-diffusion-xl-1024-v1-0"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    env = environ.Env()
    env.read_env('.env')
    SECRET_KEY = env('SECRET_KEY')
    print(SECRET_KEY)
    print('-----')
    api_key = env('IMAGE_API_KEY')

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
        engine_id = "stable-diffusion-xl-1024-v1-0"
        api_host = os.getenv('API_HOST', 'https://api.stability.ai')
        api_keys = ["sk-tYk6w9Fme97inuhtUIHXkbNlsrjQoI5GKjJWaN2qCHwmrWy3","sk-MfErYuFrlHoCCAq38rjMXkI81pnsTsx0IgtCqpE23JpbUuo9","sk-qAkGDzTUQs8qYWabfoSJ7ZmlSSv4uXz28JSrA2lJtckXwFij","sk-40whWWW9vOenzVjPxPN0cSVk5HCqKXCadmiRHkEcvyJ1KmJu"]
        current_api_key_index = 0  # 現在のAPIキーのインデックス
        Style_preset = ["3d-model", "analog-film","anime","cinematic","comic-book","digital-art","enhance","fantasy-art","isometric","line-art","low-poly","modeling-compound","neon-punk","origami","photographic","pixel-art","tile-texture"]
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
                    #"Samples": 1,画像生成枚数の指定
                    #"style_preset": Style_preset[6],
                    "text_prompts": [
                        {
                            "text": prompt
                        },
                    #{#ネガティブプロンプト
                    #"text": "",
                    #"weight": -1.0
                    #},
                    ],
                },
            )
        # レスポンス確認
            if response.status_code == 200:
                break  # APIキーが有効な場合はループを抜けます
            else:
        # APIキーが無効な場合、次のAPIキーに切り替えます
                current_api_key_index += 1
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