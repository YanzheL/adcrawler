FROM python

MAINTAINER LI YANZHE

WORKDIR /usr/src/app

ADD ./ ./

RUN pip install -U pip \
    && pip install -r requirements.txt
