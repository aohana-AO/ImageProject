from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy

# Create your models here.
# Userモデルを取得し、カスタムユーザーモデルをサポートするために使用します
User = get_user_model()

"""
class Category(models.Model):
    category_ID = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name
"""

class Image(models.Model):
    imageID = models.AutoField(primary_key=True)
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    #category_ID = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to='img/')  # 画像を保存するディレクトリを指定
    prompt = models.CharField(max_length=255,default='')
    negative_prompt = models.CharField(max_length=255,default='')



    def __str__(self):
        return f"Image {self.imageID} - User: {self.user_ID}"

