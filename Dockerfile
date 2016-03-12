# use base python image with python 2.7
FROM python:2.7

# add requirements.txt to the image
ADD requirements.txt /app/requirements.txt

# set working directory to /app/
WORKDIR /app/

# copy files from directory (in future could be git checkout
COPY stream-framework-flask.py  setup.py README.md /app/
ADD  stream_framework /app/stream_framework
#ENV PYTHONPATH /app

# install mod'ed version of stream_framework
RUN python setup.py install

# install python dependencies
RUN pip install -r requirements.txt
RUN pip install pytest mock

# create unprivileged user
RUN adduser --disabled-password --gecos '' myuser

COPY celeryconfig.py  /app/
COPY basic_eg2.py  /app/





