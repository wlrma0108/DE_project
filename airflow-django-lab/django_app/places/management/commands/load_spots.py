from django.core.management.base import BaseCommand
from places.models import Spot

class Command(BaseCommand):
    help = "데모용: 더미 관광지/평점 적재"

    def handle(self, *args, **options):
        data = [
            ("남산타워", 4.5),
            ("경복궁", 4.7),
            ("해운대", 4.2),
        ]
        created = 0
        for name, rating in data:
            obj, is_created = Spot.objects.update_or_create(
                name=name, defaults={"rating": rating}
            )
            created += 1 if is_created else 0

        self.stdout.write(self.style.SUCCESS(f"적재 완료 (신규 {created}건)"))
