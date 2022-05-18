FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /main
COPY requirements.txt /main/requirements.txt
RUN pip install -r requirements.txt
COPY . /main
