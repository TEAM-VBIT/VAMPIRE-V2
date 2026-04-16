FROM python:3.11-slim

WORKDIR /app

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ffmpeg curl unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install -U pip && pip3 install -U -r requirements.txt

COPY . .

CMD ["bash", "start"]
