

def detect_objects(tf_serving_url,images,file_names=None):
    """
    引数の画像を指定された物体検出APIに渡してその結果を返す。

    Parameters
    ----------
    tf_serving_url : str
        TensorFlow ServingのURL
    
    images : list of PIL.Image.Image
        Pillowの画像オブジェクト
    
    file_names : list of str, default None
        imagesの各画像のファイル名

    Returns
    --------------------
    detection_result: list of dicts
        物体検出結果
    """
    pass

    # 画像の配列(4次元リスト)を作成
    # 



def classify(tf_serving_url,images,file_names=None):
    """
    引数の画像を指定された画像分類APIに渡してその結果を返す

    Parameters
    ----------
    tf_serving_url : str
        TensorFlow ServingのURL
    
    images : list of PIL.Image.Image
        Pillowの画像オブジェクト
    
    file_names : list of str, default None
        imagesの各画像のファイル名

    Returns
    --------------------
    classification_result: list of dicts
        緯度、経度、撮影日時？
    """
    pass