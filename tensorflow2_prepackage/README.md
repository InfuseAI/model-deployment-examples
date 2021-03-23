# Tensorflow2 Prepackage Example

## How to build the base image

```
cd base_image
docker build . -t tensorflow2-prepackage
```

## How to use base image to build image with model file

Here we use mnist as the example. You can use the same way in other applications.

```
cd train_and_build
docker build . -t tensorflow2-prepackage-model
```

Running the built image.

```
docker run -p 9000:9000 --rm tensorflow2-prepackage-model
```

Submit a post request to test.

```
./query_by_tensor.sh
```