from django.db import migrations
from Reservation_App.models import PitchType, Cities


def populate(apps, schema_editor):
    Cities.objects.create(name="Warszawa")
    Cities.objects.create(name="Kraków")
    PitchType.objects.create(type=1)
    PitchType.objects.create(type=2)
    PitchType.objects.create(type=3)
    PitchType.objects.create(type=4)
    PitchType.objects.create(type=5)
    PitchType.objects.create(type=6)
    PitchType.objects.create(type=7)
    PitchType.objects.create(type=8)

class Migration(migrations.Migration):

    dependencies = [
        ('Reservation_App', 'initial'),
    ]

    operations = [
        migrations.RunPython(populate),
    ]