from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns =[
    path('<str:project_id>', views.get_update_task),
    path('<str:project_id>/move', views.move_task),
    path('<str:project_id>/<str:id>', views.by_id)
]