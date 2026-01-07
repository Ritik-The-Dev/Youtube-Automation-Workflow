FROM python:3.11-slim

# Prevent Python buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps for moviepy / ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy everything
COPY . /app

# Install BOTH requirements
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r ai-video-generator/requirements.txt \
    && pip install --no-cache-dir -r ai-video-uploader/requirements.txt

# Default command
CMD ["python", "orchestrator.py"]
