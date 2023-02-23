FROM python:3.10.2-bullseye

WORKDIR /opt/app/src
COPY ./requirements.txt /opt/app/src
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
# RUN python3 manage.py migrate --run-syncdb
