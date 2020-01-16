# drf-getexif

## POST

```bash
curl -X POST -F "image=@DSC_0098.JPG" http://localhost:8000/api/v1/asset/
-H "Content-Type: multipart/mixed" 
curl -i -X POST -F "image=@DSC_0098.JPG" -F "metadata={\"comment\": \"Submitting a new data set.\",\"current\": \"Submitting a new data set.\"};type=application/json" http://localhost:8000/api/v1/rectangles/

curl -i -X POST -F "image=@DSC_0098.JPG" -F "@meta.json;type=application/json" http://localhost:8000/api/v1/rectangles/

curl -i -X POST -F "image=@media/dog.jpg;image/jpeg" -F "metadata=@meta.json;type=application/json" -o "response.jpg" http://localhost:8000/api/v1/rectangles/

coreapi action rectangles create -p image=media/dog.jpg -p metadata=meta.json
```

gps
```bash
exiftool -GPSLongitudeRef=E -GPSLongitude=130.86455555555557 -GPSLatitudeRef=N -GPSLatitude=31.386555555555553 -GPSAltitude=41.47 IMGP5021.JPG
```
