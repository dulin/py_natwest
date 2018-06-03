FROM ubuntu:18.04
ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

MAINTAINER Martin Dulin <dulinoz@gmail.com>


RUN apt-get -qqy update
RUN apt-get -qqy --no-install-recommends install \
  wget \
  firefox \
  x11vnc \
  xvfb \
  xfonts-100dpi \
  xfonts-75dpi \
  xfonts-scalable \
  xfonts-cyrillic \
  python-pip \
  python-setuptools \
  python-mysqldb \
  libmysqlclient-dev \
  gcc \
  python-dev \
  python-wheel \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN pip install selenium
RUN useradd -d /home/seleuser -m seleuser
RUN mkdir -p /home/seleuser/chrome
RUN chown -R seleuser /home/seleuser
RUN chgrp -R seleuser /home/seleuser

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.20.1/geckodriver-v0.20.1-linux64.tar.gz -O /tmp/geckodriver.tar.gz \
  && tar -xzf /tmp/geckodriver.tar.gz -C /usr/bin && rm -rf /tmp/geckodriver.tar.gz

COPY requirements.txt natwest /opt/natwest/
COPY lib /opt/natwest/lib
WORKDIR /opt/natwest/
RUN mkdir tmp && touch geckodriver.log && chmod 777 tmp && chmod 777 geckodriver.log
RUN pip install -r requirements.txt
USER seleuser
CMD ./natwest


