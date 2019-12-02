import cv2
import numpy
from django.shortcuts import render
from django.core.files import File
from django.http import QueryDict, HttpResponse
from rest_framework import views, viewsets
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser
from rest_framework.response import Response
import json
from .models import Sample
from .serializers import (
    SampleSerializer,
    ImageSerializer,
    InputSerializer,
    MetadataSerializer,
    ProductSerializer
)
import io
from rest_framework.parsers import JSONParser

from PIL import Image, ImageDraw
import base64
class ProductAPIView(views.APIView):
    # parser_classes = (MultiPartParser,)

    def get_serializer(self):
        return ProductSerializer()

    def post(self, request):
        print(request.data["contentData"])
        
        b64decoded_data = base64.b64decode(request.data['encoded_data']).decode('UTF-8')
        data = JSONParser().parse(b64decoded_data)
        # serializer = ProductSerializer(data=request.data)
        # if not serializer.is_valid():
        #     return Response(serializer.errors)
        # return Response(serializer.validated_data)


class RectanglesAPIView(views.APIView):
    parser_classes = (MultiPartParser,)

    def get_serializer(self):
        return InputSerializer()

    def post(self, request):
        # receive image files
        print(request.data)
        print(request.data["metadata"])
        # print(type(request.data["metadata"]))
        # print(request.POST["metadata"])
        serializer = InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        validated_image = serializer.validated_data["image"]
        validated_json = serializer.validated_data["metadata"]
        json_dict = json.load(validated_json)
        print(json_dict)

        metadata_serializer = MetadataSerializer(data=json_dict, many=True)

        img = Image.open(validated_image).convert("RGB")
        print("img",type(img))
        draw = ImageDraw.Draw(img)
        print("draw",type(draw))
        response = HttpResponse(content_type='image/jpg') 
        img.save("rawresponse.jpg", "JPEG") 
        img.save(response, "JPEG") 
        response['Content-Disposition'] = 'attachment; filename="piece.jpg"' 
        return response
        
        # buffer = io.BytesIO()  # メモリ上への仮保管先を生成
        # img.save(buffer, format="JPEG")  # pillowのImage.saveメソッドで仮保管先へ保存
        # response = HttpResponse(
        #     buffer.getvalue(), content_type="image/jpeg")
        # response = HttpResponse(content_type="image/jpg")
        # response["Content-Disposition"] = 'attachment;filename="response.jpg"'
        # img.save(response, "JPEG")  # pillowのImage.saveメソッドで仮保管先へ保存
        # return response

label_color_dict ={
    "unactivate":(0,255,0),
    "activate":(255,0,0),
}

############################################################

############################################################


def index(request):
    """image送信画面"""
    return render(request, "appname/index.html")


class ReceiveImageAPIView(views.APIView):
    """画像を受け取るAPI"""

    parser_classes = (MultiPartParser,)

    def post(self, request):
        # receive image files
        print(request.data)
        print(request.POST["metadata"])
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
