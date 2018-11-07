FROM python:3

WORKDIR /usr/src/app

RUN apt-get update -y && apt-get upgrade -qq -y

RUN apt-get install -y python-pip

RUN pip install influxdb

RUN apt-get install -y tcpdump

COPY . .

CMD [ "python", "./py3_test.py" ]
