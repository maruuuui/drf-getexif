# -*- coding: utf-8 -*-
import requests
import base64

# ★ポイント1
XLSX_MIMETYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
JPEG_MIMETYPE = "image/jpeg"

# main
if __name__ == "__main__":

    # ★ポイント2
    uploadData = {
        "fileName": "test.png",
        "contentType": JPEG_MIMETYPE,
        # 'contentData': は別途設定
    }

    # ★ポイント3
    fileDataBinary = open("test.png", "rb").read()
    uploadData["contentData"] = base64.b64encode(fileDataBinary)

    # ★ポイント4
    url = "http://localhost:8000/api/v1/product/"
    print(base64.b64encode(fileDataBinary))
    response = requests.post(url, json=uploadData)

    print(response.status_code)
    print(response.content)
