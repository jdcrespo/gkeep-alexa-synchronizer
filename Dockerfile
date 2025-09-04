FROM arm32v7/python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Set the entrypoint
CMD ["python", "main.py"]
