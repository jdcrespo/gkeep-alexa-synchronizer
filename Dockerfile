FROM arm32v7/python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libgmp-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

RUN ls -l

# Set the entrypoint
CMD ["python", "-u", "app.py"]
