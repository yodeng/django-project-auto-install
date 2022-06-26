from django.conf.urls import url, include
from django.contrib import admin

from . import views

app_name = "run"

urlpatterns = [
    url(r'^kpipestart/?', views.kpipestart, name="kpipestart"),
]
