from . import views
from django.urls import path

urlpatterns = [
    path('', views.home,name='home'),
    path('upscale/', views.upscale,name='upscale'),
    path('about/', views.about,name='about'),
    path('upscale/startprocess/', views.startprocess,name='startprocess'),
    path('progressupdate/',views.progressupdate,name='progressupdate'),
    path('startscaling/',views.startscaling,name='startscaling'),
]
