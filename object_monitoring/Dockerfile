FROM python:3.7-slim
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install git ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt --no-cache-dir
RUN git clone https://github.com/openai/CLIP.git
EXPOSE 9000

# Define basic environment variables
ENV MODEL_NAME Model
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0

# Define customized environment variables
ENV YOLO_CKPT 'yolov5x6'
ENV MONITOR_OBJECT '0'
ENV OBJECT_PROB '0.6'
ENV CLASS_LIST_NORMAL '["An image showing a person standing on the ground", "An image showing a person is safe"]'
ENV CLASS_LIST_ABNORMAL '["An image showing a person falling on the ground", "An image showing a person is not safe", "An image showing a person meets with an accident"]'
ENV ABNORMAL_THRESHOLD '0.55'
ENV RETURN_IMAGE '0'

CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE --persistence $PERSISTENCE --access-log