from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns =[
    path('<str:domain_name>/<str:reference>', views.find_logs)
]