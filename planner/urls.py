from django.urls import path
from . import views

urlpatterns = [
    path("dayplan/", views.dayplan, name="dayplan"),
    path("status/<int:status_id>/<str:value>/", views.set_status, name="set_status"),
]