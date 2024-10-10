# Step 1: Use an official Python runtime as the base image
FROM python:3.12-slim

# Step 2: Set environment variables
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Step 3: Set the working directory in the container
WORKDIR /GarmentzCode

# Step 4: Copy the current directory contents into the container at /app
COPY . /GarmentzCode

# Step 5: Install system dependencies (for image processing, TensorFlow, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean

# Step 6: Install Python dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Step 7: Expose the port the app runs on
EXPOSE 5000

# Step 8: Set the entrypoint to Gunicorn to serve the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
