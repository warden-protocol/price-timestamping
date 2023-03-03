FROM ubuntu:22.10

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

#install dependencies (python,git,rust/cargo)
RUN apt -y update && apt install -y \
  cron \
  git \
  libssl-dev \
  python3 \
  python3-pip

# Add the script to the Docker Image
ADD price-timestamping/etl_pricedumping/pricedumping.py /root/pricedumping.py

# Give execution rights on the cron scripts
RUN chmod 0644 /root/pricedumping.py

WORKDIR /root

COPY price-timestamping/etl_pricedumping/requirements.txt ./

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . .

# Add the cron job
## TODO(Matthias): use a loop in Python to run things every minute, instead of crontab.  One fewer system to worry about that way.
RUN crontab -l | { cat; echo "* * * * * python3 /root/pricedumping.py"; } | crontab -

CMD cron
