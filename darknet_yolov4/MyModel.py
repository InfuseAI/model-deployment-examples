import darknet
import cv2
from PIL import Image
from io import BytesIO

class MyModel(object):
    def __init__(self, model_uri):
        self.network, self.class_name, self.class_colors = darknet.load_network(
            './cfg/yolov4.cfg',
            './cfg/coco.data',
            model_uri, #'yolov4.weights',
            batch_size=1
        )

    def predict(self, X, feature_names = None, meta = None):
        imageStream = BytesIO(X)
        input_image = Image.open(imageStream)

        image, detections = self.image_detection(
            input_image, self.network, self.class_name, self.class_colors, .6
        )
        darknet.print_detections(detections, True)
        #cv2.imwrite(output_file, image)

        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')
        return img_byte_arr.getvalue()

    def image_detection(self, image, network, class_names, class_colors, thresh):
        # Darknet doesn't accept numpy images.
        # Create one with image we reuse for each detect
        width = darknet.network_width(network)
        height = darknet.network_height(network)
        darknet_image = darknet.make_image(width, height, 3)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(image_rgb, (width, height),
                                interpolation=cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
        darknet.free_image(darknet_image)
        image = darknet.draw_boxes(detections, image_resized, class_colors)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), detections

    def tags(self):
        return {}

    def class_names(self):
        return []

    def metrics(self):
        return []
