# Use a lightweight Python image compatible with armhf
FROM --platform=linux/arm python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the entrypoint
ENTRYPOINT ["python", "app.py"]
