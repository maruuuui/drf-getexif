import uuid
import datetime
from django.db import models

def get_source_image_path(instance, filename: str):
    filmed_date: datetime.datetime = instance.filmed_at
    int_YYYY: int = filmed_date.year
    YYYY: str = ("0000" + str(int_YYYY))[-4:]
    int_MM: int = filmed_date.month
    MM: str = ("00" + str(int_MM))[-2:]
    int_DD: int = filmed_date.day
    DD: str = ("00" + str(int_DD))[-2:]

    image_path = "source_photo/" + "/" + YYYY + "/" + MM + "/" + DD + "/" + filename
    return image_path


class Sample(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=256)
    filmed_at = models.DateTimeField()
    # lat = models.DecimalField(max_digits=9, decimal_places=6)
    # lon = models.DecimalField(max_digits=9, decimal_places=6)
    image = models.ImageField(upload_to=get_source_image_path)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
