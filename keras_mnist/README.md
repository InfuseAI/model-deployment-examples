# Keras Example - MNIST

## How to build the docker image

```
$ s2i build . seldonio/seldon-core-s2i-python3:0.18 keras-mnist
```

## How to run the docker image 

```
$ docker run -p 5000:5000 --rm keras-mnist
```

## How to submit a post request

```
$ curl -F 'binData=@test_image.jpg' localhost:5000/api/v1.0/predictions
```
