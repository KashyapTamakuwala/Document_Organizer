FROM python:3.7.16

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install -r requirements.txt
EXPOSE 7003