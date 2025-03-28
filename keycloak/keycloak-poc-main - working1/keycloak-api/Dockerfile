# Use the official Python image
FROM python:3.12

# Set the correct working directory
WORKDIR /app

# Install vim and clean up unnecessary files
RUN apt-get update && apt-get install -y vim && apt-get clean && rm -rf /var/lib/apt/lists/*


# Copy the entire project to the container
COPY . /app

# Install Poetry
RUN pip install poetry==1.7.1 

# Configure Poetry to use virtualenvs inside the container
RUN poetry config virtualenvs.create false

# Install project dependencies
RUN poetry install --no-root 

# Set PYTHONPATH to recognize imports
ENV PYTHONPATH=/app

# Set Flask environment to development for debug mode
ENV FLASK_ENV=development

# Expose port 4000 for the Flask app
EXPOSE 4000

# Run the Flask app
CMD ["poetry", "run", "python", "api/app.py", "-p", "4000"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]

