# Use the official Python image as a base image
FROM python:3.12.0-slim

# Set the working directory in the container
WORKDIR /app

# Install build dependencies and necessary libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    pkg-config \
    cmake \
    libpoppler-cpp-dev \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install Tesseract and its language packages
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-deu \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port number
EXPOSE 8501

# Healthcheck to ensure the container is healthy
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Set the entry point for the container
CMD ["streamlit", "run", "File1.py", "--server.port=8501", "--server.address=0.0.0.0"]
