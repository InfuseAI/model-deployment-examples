import os
import cv2
import torch
from CLIP.clip import clip
from PIL import Image
from io import BytesIO
import numpy as np
import json

class Model():
    def __init__(self):
        self.yolo_ckpt = os.environ.get('YOLO_CKPT', 'yolov5m')

        # TODO: extend the object list to monitor more COCO classes 
        # object_dict = {'person': 0, 'car': 3}
        self.monitor_object = int(os.environ.get('MONITOR_OBJECT', '0'))
        self.object_prob = float(os.environ.get('OBJECT_PROB', '0.6'))

        self.class_list_normal = json.loads(
            os.environ.get('CLASS_LIST_NORMAL', '["nothing"]'))
        self.class_list_abnormal = json.loads(
            os.environ.get('CLASS_LIST_ABNORMAL', '["need help", "accident"]'))
        self.class_list = self.class_list_normal + self.class_list_abnormal
        
        self.abnormal_threshold = float(os.environ.get('ABNORMAL_THRESHOLD', '0.5'))

        self.return_image = int(os.environ.get('RETURN_IMAGE', '0'))

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_yolov5 = torch.hub.load('ultralytics/yolov5', self.yolo_ckpt, force_reload=True)
        self.model_clip, self.preprocess = clip.load("ViT-B/32", device=self.device)

        self.warning_number = 0
        
    def predict(self, X, features_names=None, meta=None):
        self.warning_number = 0

        img = Image.open(BytesIO(X))
        img = np.array(img).astype(np.uint8)
        bbox = self.predict_yolov5(img)

        ret = []
        for obj in bbox:
            if obj[5] != self.monitor_object or obj[4] < self.object_prob:
                continue
            print(obj)

            tmp = []
            tmp.append(obj)
            crop_img = img[int(obj[1]):int(obj[3]), 
                            int(obj[0]):int(obj[2])]
            probs = self.predict_clip(crop_img)[0]

            for i in range(len(self.class_list)):
                print(f"{self.class_list[i]}: {probs[i]}")
                tmp.append(f"{self.class_list[i]}: {probs[i]}")
            ret.append(tmp)
        
            if sum(probs[len(self.class_list_normal):]) >= self.abnormal_threshold:
                self.warning_number = 1
            
            if self.return_image:
                draw_color = [255, 0, 0] if \
                    sum(probs[len(self.class_list_normal):]) >= self.abnormal_threshold else [0, 255, 0]

                pt1 = (int(obj[0]), int(obj[1]))
                pt2 = (int(obj[2]), int(obj[3]))

                cv2.rectangle(img, pt1, pt2, draw_color, 1)
                cv2.putText(img,
                    f"Safety {sum(probs[:len(self.class_list_normal)])}",
                    (pt1[0], pt1[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    draw_color,
                    1)

        if self.return_image:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            _, encoded_image = cv2.imencode('.jpg', img)
            return encoded_image.tobytes()
        else:
            return {"result": ret}

    def predict_yolov5(self, image):
        results = self.model_yolov5(image)
        bounding_box = results.xyxy[0].tolist()
        return bounding_box

    def predict_clip(self, image_array):
        image = Image.fromarray(image_array)
        image = self.preprocess(image).unsqueeze(0).to(self.device)
        text = clip.tokenize(self.class_list).to(self.device)

        with torch.no_grad():
            logits_per_image, _ = self.model_clip(image, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()

        return probs
    
    def metrics(self):
        return [{"type": "GAUGE", "key": "object_monitor_warning", "value": self.warning_number}]
