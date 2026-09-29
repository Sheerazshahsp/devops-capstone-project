# Base image
FROM python:3.9-slim

# Working directory setup
WORKDIR /app

# System dependencies install karein
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Requirements copy aur install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code copy karein
COPY service/ ./service/

# Non-root user create aur set karein (Security best practice)
RUN useradd --uid 1000 theia && chown -R theia:theia /app
USER theia

# Port expose karein
EXPOSE 8080

# Application run karne ke liye Gunicorn command
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--log-level", "info", "service:app"]
