import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_gems.settings")
django.setup()


from django_gems.jewelry.models import (
    Category,
    GoldCaratWeight,
    Jewelry,
    Metal, 
    Size, 
    StoneColor, 
    StoneType,
)


categories = Category.objects.all()
sizes = Size.objects.all()
metals = Metal.objects.all()
gold_carats = GoldCaratWeight.objects.all()
jewelries = Jewelry.objects.all()
stone_types = StoneType.objects.all()
stone_colors = StoneColor.objects.all()


