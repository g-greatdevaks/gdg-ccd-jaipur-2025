FROM python:3.11-slim

WORKDIR /app

# Copy only requirements first to leverage Docker cache.
COPY requirements.txt .

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.
COPY servers/cloudrun_server.py .

CMD ["python", "cloudrun_server.py"]
