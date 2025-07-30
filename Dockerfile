FROM python:3.11-slim

# Install Java
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk curl && \
    apt-get clean

# Create app directory
WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Set environment variable (optional)
ENV H2_JAR_PATH=/app/lib/h2.jar

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]