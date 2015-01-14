FROM dockerfile/python
MAINTAINER Chris Goller <goller@gmail.com>

RUN apt-get update
RUN apt-get install -qq -y build-essential gfortran libatlas-base-dev libffi-dev libssl-dev

WORKDIR /
RUN virtualenv venv
ADD requirements.txt requirements.txt
RUN venv/bin/pip install -r requirements.txt && rm requirements.txt
ADD requirements.docs.txt requirements.docs.txt
RUN venv/bin/pip install -r requirements.docs.txt && rm requirements.docs.txt
