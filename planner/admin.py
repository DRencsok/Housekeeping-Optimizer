from django.contrib import admin
from .models import RoomType, Room, Staff, DayPlan, RoomStatus, Assignment

admin.site.register([RoomType, Room, Staff, DayPlan, RoomStatus, Assignment])