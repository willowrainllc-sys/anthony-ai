# --- EMPIRE SWARM BASE IMAGE ---
FROM python:3.13-slim

# Install system dependencies for FFmpeg and Image Processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY swarm_requirements.txt .
RUN pip install --no-cache-dir -r swarm_requirements.txt

# Copy backend code
COPY . .

# Environment Defaults
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/swarm_backend

# Set working directory to backend for execution
WORKDIR /app/swarm_backend

# Launch Command (Overridden by Docker Compose)
CMD ["python", "nexus_core.py"]
