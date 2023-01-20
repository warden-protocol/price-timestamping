FROM python:3.9
EXPOSE 6501

WORKDIR /usr/src/app

COPY price-timestamping/hash_api/src/requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN  apt-get -y update && \
     apt-get install -y pkg-config \
     apt-get install -y libssl-dev \
                    curl https://sh.rustup.rs -sSf | sh -s -- -y