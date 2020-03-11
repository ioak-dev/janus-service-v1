from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns =[
    path('', views.get_update_task),
    path('<str:id>', views.delete_task),
    path('id/<str:id>', views.get_by_id),
    path('id/<str:id>/stageId/<str:stageId>', views.move_task)
]