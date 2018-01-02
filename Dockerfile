FROM python:2.7.14-alpine
MAINTAINER Martin Dulin

COPY . /opt/natwest/
WORKDIR /opt/natwest/
RUN pip install -r requirements.txt
# todo firefox and https://github.com/mozilla/geckodriver/