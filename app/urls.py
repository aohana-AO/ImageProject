from django.urls import path

from . import views
from .views import image_detail_view

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('images/<int:image_id>/', image_detail_view, name='image_detail'),

]