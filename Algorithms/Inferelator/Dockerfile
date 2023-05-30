
FROM continuumio/anaconda3:2018.12

LABEL Maintainer="Clara Renou"

USER root

RUN apt-get update

RUN conda install -r requirements.txt

COPY runInferelator.py /

RUN mkdir data/

RUN apt-get install time
