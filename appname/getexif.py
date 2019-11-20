"""
    JPEG画像のExifから必要な情報を得る関数
    https://news.mynavi.jp/article/zeropython-42/
"""
import sys
from PIL import Image
import PIL.ExifTags as ExifTags


def get_exif_of_image(fname):
    """
    Returns
    --------------------
    exif_dict: dict
        緯度、経度、撮影日時？
    """
    exif_dict = {}
    # 画像ファイルを開く
    im = Image.open(fname)
    # EXIF情報を辞書型で得る
    exifdata = im._getexif()
    if not exifdata:
        return exif_dict
    exif = {ExifTags.TAGS[k]: v for k, v in exifdata.items() if k in ExifTags.TAGS}
    # GPS情報を得る
    gps_tags = exif["GPSInfo"]
    gps = {ExifTags.GPSTAGS.get(t, t): gps_tags[t] for t in gps_tags}

    def conv_deg(v):
        # 分数を度に変換
        d = float(v[0][0]) / float(v[0][1])
        m = float(v[1][0]) / float(v[1][1])
        s = float(v[2][0]) / float(v[2][1])
        return d + (m / 60.0) + (s / 3600.0)

    # 緯度経度情報を得る
    if gps_tags:
        lat = conv_deg(gps["GPSLatitude"])
        lat_ref = gps["GPSLatitudeRef"]
        if lat_ref != "N":
            lat = 0 - lat
        lon = conv_deg(gps["GPSLongitude"])
        lon_ref = gps["GPSLongitudeRef"]
        if lon_ref != "E":
            lon = 0 - lon
        exif_dict["lan"] = lat
        exif_dict["lon"] = lon

    # 撮影時刻を取得
    filmed_datetime = exif["DateTimeOriginal"]
    exif_dict["filmed_datetime"] = filmed_datetime

    print(exif_dict)
    return exif_dict


if __name__ == "__main__":
    exif_dict = get_exif_of_image(sys.argv[1])
    print(exif_dict)
