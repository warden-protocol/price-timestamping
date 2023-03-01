FROM ubuntu:20.04

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

#install dependencies (python,git,rust/cargo)
RUN  apt-get -y update
RUN apt install -y python3.9
RUN apt install -y python3-pip
RUN apt install -y git
RUN apt-get -y install cron
RUN apt-get install -y libssl-dev

# Add the script to the Docker Image
ADD price-timestamping/etl_pricedumping/pricedumping.py /root/pricedumping.py

# Give execution rights on the cron scripts
RUN chmod 0644 /root/pricedumping.py

WORKDIR /root

COPY price-timestamping/etl_pricedumping/requirements.txt ./

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

# Add the cron job
RUN crontab -l | { cat; echo "* * * * * python3 /root/pricedumping.py"; } | crontab -

CMD cron
