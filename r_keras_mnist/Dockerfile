FROM rocker/r-apt:bionic

RUN apt-get update && \
    apt-get install -y -qq \
        r-cran-plumber \
        r-cran-jsonlite \
        r-cran-optparse \
        r-cran-stringr \
        r-cran-urltools \
        r-cran-caret \
        curl

ENV MODEL_NAME mnist.R
ENV API_TYPE REST
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0

RUN mkdir microservice
COPY . /microservice
WORKDIR /microservice

RUN curl -OL https://raw.githubusercontent.com/SeldonIO/seldon-core/master/incubating/wrappers/s2i/R/microservice.R > /microservice/microservice.R
RUN Rscript install.R

EXPOSE 5000
CMD Rscript microservice.R --model $MODEL_NAME --api $API_TYPE --service $SERVICE_TYPE --persistence $PERSISTENCE