FROM python:3-alpine

COPY requirements.txt /requirements.txt
RUN pip install flask
RUN rm requirements.txt

COPY ./ /recipy
WORKDIR /recipy
CMD python server.py