from PIL import Image

import numpy as np
import requests

def create_request_data(images):
    image_list = []
    for image in images:
        image = Image.open(i).convert("RGB")
        (im_width, im_height) = image.size
        img_array = np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)
        tmp = img_array.tolist()
        image_list.append(tmp)
    return '{"instances" : %s}' % image_list

def format_response_data(outputs, class_name_list, file_names=None):
    #print(outputs)
    result_list = []
    for index, output_dict in enumerate(outputs):
        num_detections = int(output_dict["num_detections"])
        detection_classes = np.array(output_dict["detection_classes"]).astype(np.uint8)
        detection_scores = np.array(output_dict["detection_scores"])
        detection_boxes = np.array(output_dict["detection_boxes"])

        new_list = []

        for i in range(num_detections):
            temp_dict = {}
            if file_names:
                temp_dict["source_file_name"] = file_names[index]
            temp_dict["class_id"] = detection_classes[i]
            temp_dict["class_name"] = class_name_list[detection_classes[i]]
            temp_dict["score"] = detection_scores[i]
            detection_box = detection_boxes[i]
            box = {}
            box["min_y"] = detection_box[0]
            box["min_x"] = detection_box[1]
            box["max_y"] = detection_box[2]
            box["max_x"] = detection_box[3]
            temp_dict["box"] = box
            new_list.append(temp_dict)
        result_list.append(new_list)
    return result_list

def detection(tf_serving_url, images, class_name_list, file_names=None):

    server_url = tf_serving_url

    request_server = requests.post(server_url, data=create_request_data(images))
    print(request_server.text)
    detection_results = format_response_data(request_server.json()['predictions'],
                            class_name_list, file_names=file_names)
    print(detection_results)
    return detection_results



if __name__ == "__main__":
    class_name_list = ["a", "b", "c", "d", "e", "f", "a", "b", "c", "d",
                   "e", "f", "a", "b", "c", "d", "e", "f", "a", "b", "c", "d", "e", "f"]

    images = ["bicycle.jpg", "bicycle.jpg"]
    open_image = []
    for i in images:
        image = Image.open(i).convert("RGB")
        image = image.resize((600, 600))
        open_image.append(image)
    detection('http://10.208.136.73:8501/v1/models/od:predict', open_image,
    class_name_list, file_names=images)
