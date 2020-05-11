from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns =[
    path('', views.get_update_team),
    path('<str:id>', views.get_delete_by_id)
]