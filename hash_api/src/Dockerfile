FROM ubuntu:20.04

RUN  apt-get -y update 
RUN apt-get install -y pkg-config 
RUN apt-get install -y libssl-dev 
RUN apt install python3-pip 
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

#FROM python:3.9
EXPOSE 6501

WORKDIR /usr/src/app

COPY price-timestamping/hash_api/src/requirements.txt ./

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .
