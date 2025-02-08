FROM python:3.10-slim

WORKDIR /scripts

COPY requirements.txt ./

RUN apt-get update && apt-get install -y \
    wget unzip curl \
    chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "entrypoint.py"]
