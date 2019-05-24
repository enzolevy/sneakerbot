FROM ubuntu:latest
MAINTAINER Frederic Enard "frederic.enard@gmail.com"

RUN apt-get update -y

#Utils

RUN apt-get install -y wget curl unzip

#Python

RUN apt-get install -y python3-pip python3-dev build-essential

#Google chrome 

RUN apt-get install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libfontconfig1
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb

#Source code

COPY . /app
WORKDIR /app

#Chrome driver

RUN wget https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_linux64.zip
RUN rm -f chromedriver
RUN unzip chromedriver_linux64.zip
RUN rm chromedriver_linux64.zip

#Python dependencies

RUN pip3 install -r requirements.txt

#Entrypoint

EXPOSE 5000 2222
ENTRYPOINT ["python3"]
CMD ["app.py"]