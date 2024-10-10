FROM python:3.9-slim

# Install system dependencies including gfortran
RUN apt-get update && apt-get install -y gfortran libatlas-base-dev && apt-get clean

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Command to run the application
CMD ["gunicorn", "app:app"]
