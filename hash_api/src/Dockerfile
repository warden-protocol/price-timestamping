FROM ubuntu:20.04

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

#install dependencies (python,git,rust/cargo)
RUN  apt-get -y update 
RUN apt-get install -y pkg-config 
RUN apt-get install -y libssl-dev
RUN apt install -y python3.9 
RUN apt install -y python3-pip 
RUN apt install -y git
RUN apt install -y curl
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Add .cargo/bin to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

#FROM python:3.9
EXPOSE 6501

WORKDIR /usr/src/app

COPY price-timestamping/hash_api/src/requirements.txt ./

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

# CMD python3 price-timestamping/hash_api/wsgi.py