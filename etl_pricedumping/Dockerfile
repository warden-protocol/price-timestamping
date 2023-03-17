FROM ubuntu:22.10

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

#install dependencies (python,git,rust/cargo)
RUN apt -y update && apt install -y \
  cron \
  curl \
  git \
  libssl-dev \
  pkg-config \
  python3 \
  python3-pip

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Add .cargo/bin to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

EXPOSE 6501

WORKDIR /root

COPY etl_pricedumping/requirements.txt ./

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . price-timestamping/
