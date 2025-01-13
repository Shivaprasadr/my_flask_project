FROM python:3.10-slim
WORKDIR /scripts
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["python", "keycloak_config.py"]