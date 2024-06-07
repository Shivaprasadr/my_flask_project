FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install netcat for the health check in entrypoint.sh
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

COPY . .

# Copy the entrypoint script and ensure it's executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 5000
EXPOSE 5000

# Use entrypoint.sh as the entry point
ENTRYPOINT ["/entrypoint.sh"]
