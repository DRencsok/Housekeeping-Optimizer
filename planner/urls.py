from django.urls import path
from . import views

urlpatterns = [
    path("dayplan/", views.dayplan, name="dayplan"),
]