import base64
import io
from PIL import Image


def img_to_txt(filename):
    # msg = b"<plain_txt_msg:img>"
    with open(filename, "rb") as imageFile:
        msg = base64.b64encode(imageFile.read())
    # msg = msg + b"<!plain_txt_msg>"
    return msg


def decode_img(msg):
    # msg = msg[msg.find(b"<plain_txt_msg:img>")+len(b"<plain_txt_msg:img>"):
    #           msg.find(b"<!plain_txt_msg>")]
    msg = base64.b64decode(msg)
    buf = io.BytesIO(msg)
    img = Image.open(buf)
    return img


filename = "test.png"
msg = img_to_txt(filename)
print(msg)
img = decode_img(msg)
img.show()
