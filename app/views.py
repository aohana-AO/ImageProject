from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import View

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/index.html')

    def post(self, request, *args, **kwargs):
        image_name = request.POST.get('image_name')

        print(image_name)

        # ここで画像の処理を実装する。例えば、画像名に基づいて画像を取得してHttpResponseを返す。
        # response = ...

        return render(request, 'app/index.html')