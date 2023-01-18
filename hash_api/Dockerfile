FROM python:3.9
EXPOSE 6501

WORKDIR /code

COPY src/requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .