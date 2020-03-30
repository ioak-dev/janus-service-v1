from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns =[
    path('create', views.create),
    path('<str:spaceId>', views.get_space),
    path('banner/<str:spaceId>', views.get_banner),
    path('stage/<str:spaceId>', views.add_stage)
]