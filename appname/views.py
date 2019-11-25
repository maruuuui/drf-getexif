import cv2
import numpy
from django.shortcuts import render
from django.http import QueryDict
from rest_framework import views, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import Sample
from .serializers import SampleSerializer, ImageSerializer  # , ImageListSerializer


# class ReceiveImageAPIViewMod(views.APIView):
#     """画像を受け取るAPI改"""

#     parser_classes = (MultiPartParser,)

#     def post(self, request):
#         # receive image files
#         print(request.data)
#         files = request.data.getlist("image")
#         print(files)

#         response_arr = []

#         serializer = ImageListSerializer(data=request.data)

#         if not serializer.is_valid():
#             print("invalid!!!")
#             print(serializer.errors)
#             return Response(serializer.errors)
#         print(serializer.validated_data)
#         # validated_image = serializer.validated_data["image"]

#         return Response({"img_arr": "response_arr"})


def index(request):
    """image送信画面"""
    return render(request, "appname/index.html")


class ReceiveImageAPIView(views.APIView):
    """画像を受け取るAPI"""

    parser_classes = (MultiPartParser,)

    def post(self, request):
        # receive image files
        print(request.data)
        files = request.data.getlist("image")
        print(files)

        response_arr = []
        for received_file in files:
            # print(received_file)
            request_dict = {"image": received_file}
            new_request = QueryDict(mutable=True)
            new_request.update(request_dict)
            # print(new_request)
            serializer = ImageSerializer(data=new_request)

            if not serializer.is_valid():
                print("invalid!!!")
                print(serializer.errors)
                return Response(serializer.errors)
            print("validated_data:", serializer.validated_data)
            validated_image = serializer.validated_data["image"]
            # print(type(validated_image))
            # print(validated_image)

            # convert into numpy array
            img_arr = cv2.imdecode(
                numpy.fromstring(validated_image.read(), numpy.uint8),
                cv2.IMREAD_UNCHANGED,
            )
            response_arr.append(img_arr[:3, :3, :3])

        return Response({"img_arr": response_arr})


class SampleViewSet(viewsets.ModelViewSet):

    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
