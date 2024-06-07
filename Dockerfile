FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install nmap for the ncat command used in entrypoint.sh
RUN apt-get update && apt-get install -y nmap && apt-get clean

# Create a directory for cache files
RUN mkdir /tmp/flask_cache

COPY . .

# Copy the entrypoint script and ensure it's executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 5000
EXPOSE 5000

# Use entrypoint.sh as the entry point
ENTRYPOINT ["/entrypoint.sh"]
