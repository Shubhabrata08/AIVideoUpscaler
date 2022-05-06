from . import views
from django.urls import path

urlpatterns = [
    path('', views.home,name='home'),
    path('upscale/', views.upscale,name='upscale'),
    path('about/', views.about,name='about'),
]
