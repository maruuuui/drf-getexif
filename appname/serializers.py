import datetime
from rest_framework import serializers

from .models import Sample
from . import getexif


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        # fields = ["title", "filmed_at", "image", "created_at", "updated_at"]
        fields = ["id", "title", "filmed_at", "image", "created_at", "updated_at"]
        read_only_fields = ["filmed_at"]
        # extra_kwargs = {
        #     'filmed_at': {'write_only': True},
        # }

    def create(self, validated_data):
        sample = Sample(
            title=validated_data["title"],
            image=validated_data["image"],
            filmed_at=datetime.datetime(2000, 1, 1),
        )
        sample.save()

        exif_of_image = getexif.get_exif_of_image(sample.image.path)

        try:
            sample.filmed_at = datetime.datetime.strptime(
                exif_of_image["filmed_datetime"], "%Y:%m:%d %H:%M:%S"
            )
            sample.save()
        except KeyError:
            print("No filmed_datetime in exif")
        except ValueError:
            print("invalid filmed_datetime")
        return sample

