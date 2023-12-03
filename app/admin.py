from django.contrib import admin
from .models import Image  # .models はあなたのアプリケーション名に置き換えてください

# Imageモデルを管理画面に登録
admin.site.register(Image)
