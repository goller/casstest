FROM dockerfile/python
MAINTAINER Chris Goller <goller@gmail.com>

WORKDIR /
RUN pip install cassnode
