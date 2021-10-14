# Tensorflow 2 Example

## How to build the docker image

docker build . -t tensorflow2-resnet50

## How to run the docker image

docker run -p 9000:9000 --rm tensorflow2-resnet50

## How to submit a post request

./query_by_tensor.sh

## Sturcture

The training code is under train.py. Serving code is under MNISTModel.py. Model files are under folder `1` (the number is the version of the model which is a convention of tfserving).
