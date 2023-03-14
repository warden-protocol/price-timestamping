FROM python:3.11.2
EXPOSE 5501

WORKDIR /code

COPY src/requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
