FROM python:3
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
WORKDIR /app
COPY ./journal/requirements.txt .
COPY . /app
RUN pip install -r requirements.txt