import darknet
import cv2
import numpy as np

class MyModel(object):
    def __init__(self, model_uri ='/mnt/models'):
        self.network, self.class_name, self.class_colors = darknet.load_network(
            './cfg/yolov4.cfg',
            './cfg/coco.data',
            f'{model_uri}/yolov4.weights',
            batch_size=1
        )

    def predict(self, X, feature_names = None, meta = None):
        print("predict...")
        # Load and decode the image
        input_image = np.fromstring(X, np.uint8)
        decoded_image = cv2.imdecode(input_image, cv2.IMREAD_UNCHANGED)
        # Do the image object detection
        output_image, detections = self.image_detection(
            decoded_image, self.network, self.class_name, self.class_colors, .6
        )
        darknet.print_detections(detections, True)
        # Encode to JPG format
        _, encoded_image = cv2.imencode('.jpg', output_image)
        return encoded_image.tobytes()

    def image_detection(self, image, network, class_names, class_colors, thresh):
        # Darknet doesn't accept numpy images.
        # Create one with image we reuse for each detect
        width = darknet.network_width(network)
        height = darknet.network_height(network)
        darknet_image = darknet.make_image(width, height, 3)
        aspectRatio = [image.shape[0]/width, image.shape[1]/height]

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(image_rgb, (width, height),
                                interpolation=cv2.INTER_LINEAR)
        darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
        darknet.free_image(darknet_image)
        image = self.cvDrawBoxes(detections, image, class_colors, aspectRatio)
        return image, detections

    def cvDrawBoxes(self, detections, img, class_colors, aspectRatio):
        for detection in detections:
            x, y, w, h = detection[2][0],\
                detection[2][1],\
                detection[2][2],\
                detection[2][3]

            xmin = int(aspectRatio[1]*round(x - (w / 2)))
            xmax = int(aspectRatio[1]*round(x + (w / 2)))
            ymin = int(aspectRatio[0]*round(y - (h / 2)))
            ymax = int(aspectRatio[0]*round(y + (h / 2)))

            pt1 = (xmin, ymin)
            pt2 = (xmax, ymax)
            cv2.rectangle(img, pt1, pt2, class_colors[detection[0]], 1)
            cv2.putText(img,
                        f"{detection[0]}[{detection[1]}]",
                        (pt1[0], pt1[1] - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        class_colors[detection[0]],
                        2
            )
        return img
