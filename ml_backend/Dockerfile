FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required by Pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Pipenv
RUN pip install --no-cache-dir pipenv

# Copy Pipfile and Pipfile.lock before installing dependencies
COPY Pipfile Pipfile.lock ./

# Generate requirements.txt and install dependencies
RUN pipenv requirements > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose necessary volumes for models and data
VOLUME ["/app/ML_pipeline/models", "/app/data"]

# Expose API port
EXPOSE 5000

# Start the API using Pipenv
CMD ["python3", "/app/api.py"]