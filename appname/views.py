from .models import Sample
from .serializers import SampleSerializer
from rest_framework import viewsets


class SampleViewSet(viewsets.ModelViewSet):

    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
