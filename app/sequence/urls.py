from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns =[
    path('', views.get_update_sequence),
    path('<str:id>', views.delete_sequence),
    path('id/<str:id>', views.get_by_id),
    path('id/<str:field>/<str:context>', views.get_sequence)
]