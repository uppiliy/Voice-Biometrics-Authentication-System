FROM python:3.10-slim

# Install dependencies for audio processing
RUN apt-get update && \
    apt-get install -y ffmpeg libsndfile1 && \
    pip install --no-cache-dir torch torchaudio fastapi uvicorn python-multipart soundfile scipy numpy speechbrain

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
