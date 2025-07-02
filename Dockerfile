# Use an official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Set environment variable for port (Render uses 0.0.0.0:PORT)
ENV PORT=8080

# Expose the port
EXPOSE $PORT

# Run the app
CMD ["gunicorn", "main:app", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080"]
