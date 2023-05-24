 FROM python:3.8  #This is the base image upon which necessary libraries are installed
 
 USER root

 RUN pip install -r requirements.txt
 
 RUN apt-get update && apt-get install -y r-base time  #Installl time command to compute time taken
 
 RUN mkdir data/
 
