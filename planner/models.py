from django.db import models

class RoomType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    checkout_minutes = models.PositiveSmallIntegerField()
    stayover_minutes = models.PositiveSmallIntegerField()
    vacant_minutes = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)

    floor = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT)

    class Meta:
        ordering = ["floor", "number"]

    def __str__(self):
        return self.number


class Staff(models.Model):
    name = models.CharField(max_length=50)

    shift_start = models.TimeField(default="08:00")
    shift_minutes = models.PositiveSmallIntegerField(default=390)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "staff"

    def __str__(self):
            return self.name

class RoomStatusChoice(models.TextChoices):
    CHECKOUT = "checkout", "Checkout"
    STAYOVER = "stayover", "Stay-over"
    VACANT = "vacant", "Vacant"
    OUT_OF_ORDER = "ooo", "Out of Order"    

class DayPlan(models.Model):
    date = models.DateField(unique=True)
    created_at =models.DateTimeField(auto_now_add=True)  

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return str(self.date)

class RoomStatus(models.Model):
    day_plan = models.ForeignKey(DayPlan, on_delete=models.CASCADE, related_name="room_statuses")
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=RoomStatusChoice.choices)
    is_vip = models.BooleanField(default=True)
    vip_extra_minutes = models.PositiveSmallIntegerField(default=0)
    ready_by = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "room statuses"
        constraints = [
            models.UniqueConstraint(fields=["day_plan", "room"], name="one_status_per_room_per_day"),
        ]

    @property
    def minutes(self):
        room_type = self.room.room_type
        base = {
            RoomStatusChoice.CHECKOUT: room_type.checkout_minutes,
            RoomStatusChoice.VACANT: room_type.vacant_minutes,
            RoomStatusChoice.STAYOVER: room_type.stayover_minutes,
            RoomStatusChoice.OUT_OF_ORDER: 0,
        }[self.status]
        return base + self.vip_extra_minutes

    def __str__(self):
        return f"{self.room} - {self.get_status_display()} - ({self.day_plan})"

class Assignment(models.Model):
    room_status = models.ForeignKey(RoomStatus, on_delete=models.CASCADE, related_name="assignment")
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT)
    order = models.PositiveSmallIntegerField()
    done_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["staff", "order"]

    def __str__(self):
        return f"{self.staff}: {self.room_status.room} (#{self.order}) "