FROM ubuntu:20.04

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

#install dependencies (python,git,rust/cargo)
RUN apt -y update && apt install -y \
  pkg-config \
  libssl-dev \
  python3 \
  python3-pip \
  git \
  curl
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

EXPOSE 6501

WORKDIR /usr/src/app

COPY price-timestamping/hash_api/src/requirements.txt ./

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .
