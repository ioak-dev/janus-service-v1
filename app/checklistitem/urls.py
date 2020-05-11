from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns =[
    path('task/<str:task_id>', views.get_by_taskid),
    path('', views.update_checklistitem),
    path('<str:id>', views.delete_checklistitem)
]