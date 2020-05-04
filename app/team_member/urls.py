from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns =[
    path('<str:team_id>/<str:user_id>', views.post_delete),
    path('', views.get),
    path('<str:id>', views.delete_by_id)
]