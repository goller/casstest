FROM dockerfile/python
MAINTAINER Chris Goller <goller@gmail.com>

RUN apt-get update
RUN apt-get install -qq -y build-essential python-dev libev4 libev-dev
WORKDIR /
RUN pip install casstest
