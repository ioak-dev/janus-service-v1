from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns =[
    path('', views.get_update_comment),
    path('<str:id>', views.delete_comment),
    path('id/<str:id>', views.get_by_id)
]