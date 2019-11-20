import cv2
import numpy
from django.shortcuts import render
from rest_framework import views, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import Sample
from .serializers import SampleSerializer


def index(request):
    """image送信画面"""
    return render(request, "appname/index.html")


class ReceiveImageAPIView(views.APIView):
    """画像を受け取るAPI"""
    parser_classes = (MultiPartParser,)

    def post(self, request):
        # receive image files
        print(request.data)
        received_image = request.FILES['image']
        print(type(received_image))
        print(received_image)

        # convert into numpy array
        img_arr = cv2.imdecode(numpy.fromstring(
            received_image.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

        # print(type(img_arr))
        # print(img_arr)
        return Response({'received data': received_image.name})


class SampleViewSet(viewsets.ModelViewSet):

    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
