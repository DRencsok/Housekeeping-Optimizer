from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import DayPlan, RoomStatus, Room, RoomStatusChoice
from datetime import date

# Create your views here.

def dayplan(request):
    day_plan, created = DayPlan.objects.get_or_create(date=date.today())

    if created:
        for room in Room.objects.filter(is_active=True):
            RoomStatus.objects.create(
                day_plan = day_plan,
                room = room,
                status = "stayover",
            )
    statuses = RoomStatus.objects.filter(day_plan=day_plan)

    if request.method == "POST":
        for status in RoomStatus.objects.filter(day_plan=day_plan):
            new_value = request.POST.get(f"status_{status.id}")
            if new_value and new_value != status.status:
                status.status = new_value
                status.save()
        return redirect("dayplan")

    return render(request, "planner/dayplan.html", 
            {
        "day_plan": day_plan,
            "statuses": statuses,
            "status_choices": RoomStatusChoice.choices,
            })
