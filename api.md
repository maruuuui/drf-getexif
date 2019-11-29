# AIAPI 

## 外部とのインターフェース部分

### リクエスト

base64の中にファイル名が埋め込まれないならばファイル名の情報も別途持つ必要有り

```json
{
    "source_images":[
        {
        "base64_image": "(base64_image)", // 画像本体
        "file_name": "(filename)"        // ファイル名
        }
    ],
    "output_overlayed_image":true // 処理後の画像も返すかどうか(API内でデフォルト値を持つようにするか？)
}
```

### レスポンス

```json
[
    {
        "source_file_name":"sample_clamp.jpg",
        "detected_result":[
            {
                "detection_class_id":1,
                "detection_class_name":"clamp",
                "detection_score":0.37508297,
                "detection_box":{
                    "min_y":0.0458507836,
                    "min_x":0.0100839734,
                    "max_y":0.980554342,
                    "max_x":0.700636327
                },
                "classify_class_id":2,
                "classify_class_name":"unactuated",
                "classify_scores":[
                    {
                        "class_id":1,
                        "class_name":"actuated",
                        "score":0.48
                    },
                    {
                        "class_id":2,
                        "class_name":"unactuated",
                        "score":0.52
                    }
                ]
            }
        ],
        "overlayed_image": "base64_image"
    }
]
```

## 物体検出モデルを使用するための関数(do_detection(source_file_names,tf_serving_url)?)

### 入力

<!-- ```bash
curl -X POST https://dischargeclamp.dev.inhouse.tepsyslabs.com/api/v1/detection/ 
-F file_field_name=@image_file -k
``` -->

TFservingの条件を極めるためURLも引数に入れたほうが良い

```json
{
    "tf_serving_url":"(URL)",
    "images":[
        "image" //画像本体
    ],
    "file_names":[// ファイル名(オプション)
        "source_file1",
        "source_file2"
    ]
}
```

### 出力

```json
[
    {
        "source_file_name":"sample_clamp.jpg",
        "class_id":1,
        "class_name":"clamp", // 返り値にはdetection class以外にclass名も必要
        "score":0.37508297,
        "box":{
            "min_y":0.0458507836,
            "min_x":0.0100839734,
            "max_y":0.980554342,
            "max_x":0.700636327
        }
    }
]
```

## 画像分類モデル用関数(classificate())

### リクエスト

```bash
curl -X POST curl -X POST https://dischargeclamp.dev.inhouse.tepsyslabs.com/api/v1/classify/ 
-F file_field_name=@image_file -k
```

```json
{
    "tf_serving_url":"(URL)",
    "images":[
        "image" //画像本体
    ],
    "file_names":[// ファイル名(オプション)
        "source_file1",
        "source_file2"
    ]
}
```

### レスポンス

```json
[
    {
        "file_name":"sample_clamp_001.jpg", //file_namesが入力にあれば
        "class_id":2,
        "class_name":"unactuated",
        "scores":[
            {
                "class_id":1,
                "class_name":"actuated",
                "score":0.48
            },
            {
                "class_id":2,
                "class_name":"unactuated",
                "score":0.52
            }
        ]
    }
]
```

## 検出結果描画

### リクエスト

```bash
curl -X POST http://127.0.0.1:8000/api/v1/overlay-image/ -F file_field_name=@sample_clamp.jpg -F 
"inference_data=
{
    \"inference_data\":[
        {
            \"topleft\":{
                \"y\":0.0458507836,
                \"x\":0.0100839734,
            },
            \"bottomright\":{
                \"y\":0.980554342,
                \"x\":0.700636327,
            },
            \"inference\":{
                \"label\":\"actuated\",
                \"score\":0.48
            }
        },
        {
            \"topleft\":{
                \"y\":0.1058507836,
                \"x\":0.2000839734,
            },
            \"bottomright\":{
                \"y\":0.650554342,
                \"x\":0.500636327,
            },
            \"inference\":{
                \"label\":\"unactuated\",
                \"score\":0.52
            }
        }
    ]
}
"
-o result.jpg
```

```json
{
    "source_images":[
        "image" //ベース画像本体(どの型で渡す？)
    ],
    "source_file_names":[// ファイル名(オプション)
        "source_file1",
        "source_file2"
    ],
    "detection_data":[
        {
            "source_file_name":"sample_clamp.jpg",
            "class_id":1,
            "class_name":"clamp", // 返り値にはdetection class以外にclass名も必要
            "score":0.37508297,
            "box":{
                "min_y":0.0458507836,
                "min_x":0.0100839734,
                "max_y":0.980554342,
                "max_x":0.700636327
            }
        }
    ],
    "classification_data":[ //あればdetection_dataとマージして処理する(オプション)
        {
            "file_name":"sample_clamp_001.jpg",
            "class_id":2,
            "class_name":"unactuated",
            "scores":[
                {
                    "class_id":1,
                    "class_name":"actuated",
                    "score":0.48
                },
                {
                    "class_id":2,
                    "class_name":"unactuated",
                    "score":0.52
                }
            ]
        }
    ]
}
```

### レスポンス

"overlayed_images": ["処理後画像"]

## task

- 関数内で渡す画像の型の設定
- base64エンコードされた文字列にファイル名のデータは含まれる？
- base64には元のファイル名の情報は含まれる？

<!-- 
API部分ここまで
 -->

## ファイルアップロード

### リクエスト

"
{
	"memo":"(text)",
    "source_images":[
        {
        "base64_image": "(base64_image)", // 画像本体
        "file_name": "(filename)"        // ファイル名
        }
    ]
}

### 内部処理
1.DBに画像情報を保存（exifデータ含む）
2.S3に画像ファイルを保存

### レスポンス
成功:200
失敗:500,エラーメッセージ
失敗:400,エラーメッセージ




## Lambda

lambda
・S3にファイルが上がるとうごく
・S3に上がった画像ファイル名（UUID）を放電クランプのAPIに渡すだけ
	lambdaをqueueに置き換えできる
	
	

## 放電クランプAPI本体

### リクエスト(POST)

{
"source_images_uuid":[
(UUID),

]
}
### レスポンス
成功:200,完了画像キー
失敗:500,エラーメッセージ
失敗:400,エラーメッセージ

### 完了後の標準出力
成功:success,完了画像キー
失敗:fail,エラーメッセージ


# ## S3バケット（temp）
# /yyyy/mm/dd/(UUID)/(originalFilename).jpg

## 永続S3バケット
/static
/media
	/yyyy/mm/dd/(UUID)
		/source
			/(originalFilename).jpg
		/retouched
			/(originalFilename).jpg
		/overlayed
			/(originalFilename).jpg
		/crop
			/1
				/(originalFilename).jpg
			/2
			/3

## DB
source_image
	id(uuid),
	name,
	point,
	filming_datetime,
	photo_url(永続S3パス),
	created_at,
	updatedat

# temp_source_image
#	id(uuid),
#	temp_photo_url(tempS3パス)
#	created_at
#	updatedat
