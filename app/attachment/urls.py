from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns =[
    path('task/<str:task_id>', views.get_by_task_id),
    path('', views.add_attachment),
    path('<str:attachment_id>', views.download_delete_attachment)
]