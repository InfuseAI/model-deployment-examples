# Keras Example - MNIST

## How to build the docker image

```
$ docker build . -t keras-mnist
```

## How to run the docker image 

```
$ docker run -p 9000:9000 --rm keras-mnist
```

## How to submit a post request

```
$ curl -F 'binData=@test_image.jpg' localhost:9000/api/v1.0/predictions
```
