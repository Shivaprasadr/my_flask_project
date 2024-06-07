FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=flaskr
ENV FLASK_ENV=development

# Custom entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use the entrypoint script to initialize the database and start the app
ENTRYPOINT ["/entrypoint.sh"]
