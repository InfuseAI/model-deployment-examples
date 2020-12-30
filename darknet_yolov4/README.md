# Darknet YOLO v4

In this example, we demonstrate how to build a custom pre-packaged server for [AlexeyAB/darknet YOLO v4](https://github.com/AlexeyAB/darknet).

The server detect objects in an image

- **Input:** (binData) the bytes of image
- **Output:** (binData) the bytes of image with jpg format
- **Model Files:** The `yolov4.weights` described in [document](https://github.com/AlexeyAB/darknet#pre-trained-models)

  ```
  <model uri>
  └── yolov4.weights
  ```

## How to build the docker image

```
docker build -t darknet-yolov4 .
```

## How to run the docker image

1. Download the `yolov4.weights` file 245 MB: [yolov4.weights](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights)
1. Put the files at `models/`
1. Run the image

   ```
   docker run --name darknet --rm -it -p 5000:5000 -v $PWD/models:/mnt/models darknet-yolov4
   ```

## How to submit a post request

1. Prepare a picture
1. Send by curl

   ```
   curl -F 'binData=@./input.jpg' localhost:5000/api/v1.0/predictions | jq -r .binData | base64 --decode > output.jpg
   ```

1. The result goes to `output.jpg`
