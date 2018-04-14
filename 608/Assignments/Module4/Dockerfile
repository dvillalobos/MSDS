FROM ubuntu:16.04

MAINTAINER Duubar Villalobos Jimenez "mydvtech@gmail.com"

RUN apt-get update -y

RUN apt-get install -y apt-utils python3-pip python3-all python3-all-dev

RUN apt-get update -y

CMD [ "pip3", "install -U setuptools"]


# Uncomment these lines if adding csv files to Docker app
#WORKDIR /usr/src/app/riverkeeper/data
#COPY EnteroCount2006-2017.csv ./
#COPY riverkeeper_data_2013.csv ./
#COPY Riverkeeper_Stations.csv ./


WORKDIR /usr/src/app/riverkeeper
COPY requirements.txt ./
COPY data608-project04.py ./

RUN pip3 install --no-cache-dir -r requirements.txt


EXPOSE 8050
CMD [ "python3", "/usr/src/app/riverkeeper/data608-project04.py" ]
