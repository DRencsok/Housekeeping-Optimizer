from django.core.management.base import BaseCommand
from planner.models import RoomType, Room, Staff


class Command(BaseCommand):
    help = "Create a fictional 5-floor, 60-room hotel with 5 cleaners"

    def handle(self, *args, **options):
        standard, _ = RoomType.objects.get_or_create(
            name="Standard",
            defaults={"checkout_minutes": 30, "stayover_minutes": 18, "vacant_minutes": 10},
        )
        superior, _ = RoomType.objects.get_or_create(
            name="Superior",
            defaults={"checkout_minutes": 38, "stayover_minutes": 22, "vacant_minutes": 12},
        )
        suite, _ = RoomType.objects.get_or_create(
            name="Suite",
            defaults={"checkout_minutes": 55, "stayover_minutes": 30, "vacant_minutes": 15},
        )

        for floor in range(1, 6):
            for n in range(1, 13):
                if floor == 5:
                    room_type = suite if n <= 4 else superior
                elif floor >= 3:
                    room_type = superior if n <= 6 else standard
                else:
                    room_type = standard

                Room.objects.get_or_create(
                    number=f"{floor}{n:02d}",
                    defaults={"floor": floor, "room_type": room_type},
                )

        for name in ["Eva", "Marek", "Lucia", "Tomáš", "Zuzana"]:
            Staff.objects.get_or_create(name=name, defaults={"shift_minutes": 390})

        self.stdout.write(f"{Room.objects.count()} rooms, {Staff.objects.count()} staff")