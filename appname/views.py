from django.core.files.storage import default_storage
import numbers as np
import cv2
from rest_framework import views, viewsets
from rest_framework.response import Response
from django.shortcuts import HttpResponse, render, get_object_or_404

from config import settings
from .models import Sample
from .serializers import SampleSerializer, ImageSerializer

from rest_framework.parsers import MultiPartParser


def index(request):
    """image送信画面"""
    return render(request, "appname/index.html")


class ReceiveImageAPIView(views.APIView):
    """画像を受け取るAPI"""
    parser_classes = (MultiPartParser,)

    def post(self, request):
        # to access files
        received_image = request.FILES['image']
        print(type(received_image))
        print(received_image)

        filename = received_image.name  # received file name
        tmp_image_file = 'tmp/'+filename
        with default_storage.open(tmp_image_file, 'wb+') as destination:
            for chunk in received_image.chunks():
                destination.write(chunk)

        src = cv2.imread(settings.MEDIA_ROOT+"/"+tmp_image_file)
        print(src)
        return Response({'received data': received_image.name})


class SampleViewSet(viewsets.ModelViewSet):

    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
