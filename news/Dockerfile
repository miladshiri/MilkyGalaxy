# base image  
FROM python:3.8

# where your code lives  
WORKDIR /usr/src/qvikapp

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# install dependencies  
RUN pip install --upgrade pip  

# copy whole project to your docker home directory. 
COPY . .

# run this command to install all dependencies  
RUN pip install -r requirements.txt

# Build the tables
RUN python manage.py migrate

