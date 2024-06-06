FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=flaskr
# Expose port 5000
EXPOSE 5000

CMD ["flask", "--app", "flaskr", "run", "--host=0.0.0.0", "--debug"]
